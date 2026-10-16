"""Student username/password auth with a dedicated cookie JWT."""

from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, HTTPException, Request, Response, status
from pwdlib import PasswordHash
from pydantic import UUID4
from sqlalchemy.orm import Session

from lexloop.config import env_settings
from lexloop.controller import get_db
from lexloop.model.student_model import Student
from lexloop.repository import student_repository

STUDENT_COOKIE = "lexloop-studentauth"
_password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return _password_hash.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    return _password_hash.verify(password, hashed)


def create_student_token(student_id: UUID4) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(student_id),
        "principal": "student",
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(hours=12)).timestamp()),
    }
    return jwt.encode(
        payload, env_settings.JWT_SIGNING_SECRET, algorithm="HS256"
    )


def decode_student_token(token: str) -> UUID4:
    try:
        payload = jwt.decode(
            token,
            env_settings.JWT_SIGNING_SECRET,
            algorithms=["HS256"],
        )
    except jwt.PyJWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid student session",
        ) from exc
    if payload.get("principal") != "student":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid student session",
        )
    return uuid.UUID(payload["sub"])


def set_student_cookie(response: Response, token: str) -> None:
    response.set_cookie(
        key=STUDENT_COOKIE,
        value=token,
        max_age=60 * 60 * 12,
        httponly=True,
        samesite="lax",
        secure=False,
    )


def clear_student_cookie(response: Response) -> None:
    response.delete_cookie(STUDENT_COOKIE)


def get_optional_student(
    request: Request, session: Session = Depends(get_db)
) -> Student | None:
    token = request.cookies.get(STUDENT_COOKIE)
    if not token:
        return None
    try:
        student_id = decode_student_token(token)
    except HTTPException:
        return None
    row = student_repository.get_by_uuid(student_id, session)
    if row is None or not row.is_active:
        return None
    return row.to_internal_model()


def require_student(
    student: Student | None = Depends(get_optional_student),
) -> Student:
    if student is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    return student
