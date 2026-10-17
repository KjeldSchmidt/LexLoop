"""Application service for students."""

import os
from concurrent.futures import ThreadPoolExecutor
from typing import Sequence

from pydantic import UUID4
from sqlalchemy.orm import Session

from lexloop.auth.memorable_ids import generate_password, generate_username
from lexloop.auth.student_auth import hash_password, verify_password
from lexloop.model.student_model import (
    Student,
    StudentCreate,
    StudentCreatedCreds,
)
from lexloop.repository import student_repository
from lexloop.repository.student_repository import StudentInsert

_MAX_USERNAME_ATTEMPTS = 64
# pwdlib recommended Argon2 uses ~64MiB per hash; keep concurrency low on Lambda.
_HASH_WORKERS = 8
_ARGON2_MIB_PER_HASH = 96
_LAMBDA_RESERVED_MIB = 256


def create_for_teacher(
    payload: StudentCreate, teacher_id: UUID4, session: Session
) -> Student:
    existing = student_repository.get_by_username(payload.username, session)
    if existing is not None:
        raise ValueError("USERNAME_TAKEN")
    return student_repository.add(
        payload, hash_password(payload.password), teacher_id, session
    )


def bulk_create_for_teacher(
    count: int, teacher_id: UUID4, session: Session
) -> list[StudentCreatedCreds]:
    """Create ``count`` students with memorable usernames and phrase passwords.

    Password hashing runs in a thread pool (Argon2 releases the GIL). All rows
    are inserted in one DB transaction.
    """
    usernames = _unique_usernames(count, session)
    passwords = [generate_password() for _ in range(count)]
    hashed = _hash_passwords(passwords)
    inserts = [
        StudentInsert(username=username, hashed_password=hashed_password)
        for username, hashed_password in zip(usernames, hashed, strict=True)
    ]
    students = student_repository.add_many(inserts, teacher_id, session)
    return [
        StudentCreatedCreds(
            uuid=student.uuid,
            username=student.username,
            password=password,
            is_active=student.is_active,
        )
        for student, password in zip(students, passwords, strict=True)
    ]


def _unique_usernames(count: int, session: Session) -> list[str]:
    """Generate ``count`` usernames that are unique in-memory and in the DB."""
    chosen: list[str] = []
    chosen_set: set[str] = set()
    attempts = 0
    max_attempts = max(_MAX_USERNAME_ATTEMPTS, count * 4)
    while len(chosen) < count:
        attempts += 1
        if attempts > max_attempts:
            raise RuntimeError("USERNAME_GENERATION_FAILED")
        candidate = generate_username(with_numeric_suffix=attempts > count * 2)
        if candidate in chosen_set:
            continue
        chosen.append(candidate)
        chosen_set.add(candidate)

    taken = student_repository.usernames_in_use(chosen_set, session)
    if not taken:
        return chosen

    # Replace collisions without restarting the whole batch.
    replacements: list[str] = []
    replacement_set = set(chosen_set)
    while len(replacements) < len(taken):
        attempts += 1
        if attempts > max_attempts * 2:
            raise RuntimeError("USERNAME_GENERATION_FAILED")
        candidate = generate_username(with_numeric_suffix=True)
        if candidate in replacement_set or candidate in taken:
            continue
        replacements.append(candidate)
        replacement_set.add(candidate)
    still_taken = student_repository.usernames_in_use(
        set(replacements), session
    )
    if still_taken:
        raise RuntimeError("USERNAME_GENERATION_FAILED")

    result: list[str] = []
    replacement_iter = iter(replacements)
    for username in chosen:
        if username in taken:
            result.append(next(replacement_iter))
        else:
            result.append(username)
    return result


def _hash_worker_count(n: int) -> int:
    """Cap parallel Argon2 hashes so Lambda does not OOM."""
    mem_mb = int(os.environ.get("AWS_LAMBDA_FUNCTION_MEMORY_SIZE", "2048"))
    max_by_mem = max(1, (mem_mb - _LAMBDA_RESERVED_MIB) // _ARGON2_MIB_PER_HASH)
    return min(_HASH_WORKERS, n, max_by_mem)


def _hash_passwords(passwords: Sequence[str]) -> list[str]:
    if len(passwords) <= 1:
        return [hash_password(p) for p in passwords]
    workers = _hash_worker_count(len(passwords))
    if workers == 1:
        return [hash_password(p) for p in passwords]
    with ThreadPoolExecutor(max_workers=workers) as pool:
        return list(pool.map(hash_password, passwords))


def list_for_teacher(teacher_id: UUID4, session: Session) -> list[Student]:
    return student_repository.list_for_teacher(teacher_id, session)


def authenticate(
    username: str, password: str, session: Session
) -> Student | None:
    row = student_repository.get_by_username(username, session)
    if row is None or not row.is_active:
        return None
    if not verify_password(password, row.hashed_password):
        return None
    return row.to_internal_model()


def reset_password(
    student_uuid: UUID4,
    teacher_id: UUID4,
    new_password: str,
    session: Session,
) -> Student:
    row = student_repository.get_by_uuid(student_uuid, session)
    if row is None or row.created_by_teacher_id != teacher_id:
        raise KeyError
    return student_repository.set_password(
        student_uuid, hash_password(new_password), session
    )


def set_active(
    student_uuid: UUID4,
    teacher_id: UUID4,
    is_active: bool,
    session: Session,
) -> Student:
    row = student_repository.get_by_uuid(student_uuid, session)
    if row is None or row.created_by_teacher_id != teacher_id:
        raise KeyError
    return student_repository.set_active(student_uuid, is_active, session)


def delete_for_teacher(
    student_uuid: UUID4, teacher_id: UUID4, session: Session
) -> None:
    row = student_repository.get_by_uuid(student_uuid, session)
    if row is None or row.created_by_teacher_id != teacher_id:
        raise KeyError
    student_repository.delete(student_uuid, session)


def bulk_delete_for_teacher(
    student_uuids: list[UUID4], teacher_id: UUID4, session: Session
) -> int:
    for student_uuid in student_uuids:
        row = student_repository.get_by_uuid(student_uuid, session)
        if row is None or row.created_by_teacher_id != teacher_id:
            raise KeyError
    student_repository.delete_many(student_uuids, session)
    return len(student_uuids)


def bulk_reset_passwords_for_teacher(
    student_uuids: list[UUID4], teacher_id: UUID4, session: Session
) -> list[StudentCreatedCreds]:
    """Reset passwords for owned students; return one-time plaintext phrases."""
    owned: list[Student] = []
    for student_uuid in student_uuids:
        row = student_repository.get_by_uuid(student_uuid, session)
        if row is None or row.created_by_teacher_id != teacher_id:
            raise KeyError
        owned.append(row.to_internal_model())

    passwords = [generate_password() for _ in owned]
    hashed = _hash_passwords(passwords)
    updates = [
        (student.uuid, hashed_password)
        for student, hashed_password in zip(owned, hashed, strict=True)
    ]
    students = student_repository.set_passwords(updates, session)
    return [
        StudentCreatedCreds(
            uuid=student.uuid,
            username=student.username,
            password=password,
            is_active=student.is_active,
        )
        for student, password in zip(students, passwords, strict=True)
    ]
