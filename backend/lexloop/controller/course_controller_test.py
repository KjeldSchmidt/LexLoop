import uuid

from fastapi.testclient import TestClient
from sqlalchemy import text
from sqlalchemy.orm import Session

from lexloop.auth.principal import (
    Principal,
    PrincipalKind,
    require_principal,
    require_teacher,
)
from lexloop.auth.student_auth import require_student
from lexloop.auth.user_model import User
from lexloop.main import app
from lexloop.model.student_model import Student

SEED_TEACHER_ID = uuid.UUID("11111111-1111-4111-8111-111111111111")
BASE_COURSE = "59cc5186-a10d-476e-b750-c8f5b821b953"
BASE_SIGNUP_CODE = "BASE"


def _seed_teacher() -> User:
    return User(
        id=SEED_TEACHER_ID,
        email="seed-teacher@lexloop.test",
        hashed_password="x",
        is_active=True,
        is_superuser=False,
        is_verified=True,
        role="teacher",
    )


def _student(student_uuid: uuid.UUID, teacher_id: uuid.UUID) -> Student:
    return Student(
        uuid=student_uuid,
        username="joiner",
        is_active=True,
        created_by_teacher_id=teacher_id,
    )


def test_get_courses(client: TestClient) -> None:
    response = client.get("/courses")
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 2
    assert len(body["items"]) == 2
    assert body["items"][0]["name"] == "Base Course"
    assert body["items"][0]["description"] == "Seed vocabulary course"
    assert body["items"][0]["signup_code"] == BASE_SIGNUP_CODE
    assert body["offset"] == 0
    assert body["limit"] == 50


def test_get_courses_paginated(client: TestClient) -> None:
    response = client.get("/courses", params={"limit": 1, "offset": 1})
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 2
    assert len(body["items"]) == 1
    assert body["offset"] == 1
    assert body["limit"] == 1


def test_teacher_can_create_update_delete_course(
    client: TestClient, db_session: Session
) -> None:
    app.dependency_overrides[require_teacher] = _seed_teacher

    create = client.post(
        "/courses",
        json={"course": {"name": "New Course", "description": "Hello"}},
    )
    assert create.status_code == 201
    course = create.json()
    assert course["name"] == "New Course"
    assert course["description"] == "Hello"
    assert course["owner_teacher_id"] == str(SEED_TEACHER_ID)
    assert course["signup_code"] is not None
    assert len(course["signup_code"]) == 4
    assert course["signup_code"].isalpha()
    assert course["signup_code"].isupper()
    course_uuid = course["uuid"]

    patch = client.patch(
        f"/courses/{course_uuid}",
        json={"course": {"name": "Renamed", "description": "Updated"}},
    )
    assert patch.status_code == 200
    assert patch.json()["name"] == "Renamed"
    assert patch.json()["description"] == "Updated"

    delete = client.delete(f"/courses/{course_uuid}")
    assert delete.status_code == 204
    listed = client.get("/courses")
    names = [c["name"] for c in listed.json()["items"]]
    assert "Renamed" not in names

    app.dependency_overrides.pop(require_teacher, None)


def test_teacher_can_enroll_and_unenroll_own_students(
    client: TestClient, db_session: Session
) -> None:
    app.dependency_overrides[require_teacher] = _seed_teacher

    create_student = client.post(
        "/students",
        json={"username": "enrollee01", "password": "password123"},
    )
    assert create_student.status_code == 201
    student_uuid = create_student.json()["uuid"]

    enroll = client.post(
        f"/course/{BASE_COURSE}/enrollments",
        json={"enrollment": {"student_uuids": [student_uuid]}},
    )
    assert enroll.status_code == 200
    assert enroll.json()["added"] == 1

    enrolled = client.get(f"/course/{BASE_COURSE}/students")
    assert enrolled.status_code == 200
    assert any(s["uuid"] == student_uuid for s in enrolled.json())

    # Idempotent re-enroll
    again = client.post(
        f"/course/{BASE_COURSE}/enrollments",
        json={"enrollment": {"student_uuids": [student_uuid]}},
    )
    assert again.status_code == 200
    assert again.json()["added"] == 0

    remove = client.post(
        f"/course/{BASE_COURSE}/enrollments/remove",
        json={"enrollment": {"student_uuids": [student_uuid]}},
    )
    assert remove.status_code == 200
    assert remove.json()["removed"] == 1

    enrolled_after = client.get(f"/course/{BASE_COURSE}/students")
    assert enrolled_after.json() == []

    app.dependency_overrides.pop(require_teacher, None)


def test_cannot_enroll_another_teachers_student(
    client: TestClient, db_session: Session
) -> None:
    db_session.execute(
        text(
            """
            INSERT INTO "user"
              (id, email, hashed_password, is_active, is_superuser, is_verified, role)
            VALUES
              (
                '22222222-2222-4222-8222-222222222222',
                'other@lexloop.test',
                'x',
                true,
                false,
                true,
                'teacher'
              )
            ON CONFLICT (id) DO NOTHING
            """
        )
    )
    db_session.execute(
        text(
            """
            INSERT INTO lexloop_students
              (uuid, username, hashed_password, is_active, created_by_teacher_id)
            VALUES
              (
                '33333333-3333-4333-8333-333333333333',
                'foreign_pupil',
                'x',
                true,
                '22222222-2222-4222-8222-222222222222'
              )
            """
        )
    )
    db_session.commit()

    app.dependency_overrides[require_teacher] = _seed_teacher
    enroll = client.post(
        f"/course/{BASE_COURSE}/enrollments",
        json={
            "enrollment": {
                "student_uuids": ["33333333-3333-4333-8333-333333333333"]
            }
        },
    )
    assert enroll.status_code == 400
    assert enroll.json()["detail"] == "STUDENT_NOT_OWNED"
    app.dependency_overrides.pop(require_teacher, None)


def test_student_join_request_and_teacher_approve_all(
    client: TestClient, db_session: Session
) -> None:
    """Foreign teacher's student can request; approve-all enrolls without ownership check."""
    other_teacher = uuid.UUID("22222222-2222-4222-8222-222222222222")
    student_uuid = uuid.UUID("44444444-4444-4444-8444-444444444444")
    db_session.execute(
        text(
            """
            INSERT INTO "user"
              (id, email, hashed_password, is_active, is_superuser, is_verified, role)
            VALUES
              (
                '22222222-2222-4222-8222-222222222222',
                'other2@lexloop.test',
                'x',
                true,
                false,
                true,
                'teacher'
              )
            ON CONFLICT (id) DO NOTHING
            """
        )
    )
    db_session.execute(
        text(
            """
            INSERT INTO lexloop_students
              (uuid, username, hashed_password, is_active, created_by_teacher_id)
            VALUES
              (
                '44444444-4444-4444-8444-444444444444',
                'code_joiner',
                'x',
                true,
                '22222222-2222-4222-8222-222222222222'
              )
            """
        )
    )
    db_session.commit()

    app.dependency_overrides[require_student] = lambda: _student(
        student_uuid, other_teacher
    )
    preview = client.get(f"/courses/by-code/{BASE_SIGNUP_CODE}")
    assert preview.status_code == 200
    assert preview.json()["course_name"] == "Base Course"

    request = client.post(
        "/courses/join-requests",
        json={"join_request": {"code": BASE_SIGNUP_CODE}},
    )
    assert request.status_code == 200
    assert request.json()["status"] == "pending"

    again = client.post(
        "/courses/join-requests",
        json={"join_request": {"code": "base"}},
    )
    assert again.status_code == 200
    assert again.json()["status"] == "already_pending"

    mine = client.get("/courses/join-requests")
    assert mine.status_code == 200
    assert len(mine.json()) == 1
    assert mine.json()[0]["course_uuid"] == BASE_COURSE
    assert mine.json()[0]["course_name"] == "Base Course"
    app.dependency_overrides.pop(require_student, None)

    app.dependency_overrides[require_teacher] = _seed_teacher
    pending = client.get(f"/course/{BASE_COURSE}/join-requests")
    assert pending.status_code == 200
    assert any(s["uuid"] == str(student_uuid) for s in pending.json())

    approved = client.post(f"/course/{BASE_COURSE}/join-requests/approve-all")
    assert approved.status_code == 200
    assert approved.json()["enrolled"] == 1

    enrolled = client.get(f"/course/{BASE_COURSE}/students")
    assert any(s["uuid"] == str(student_uuid) for s in enrolled.json())
    assert client.get(f"/course/{BASE_COURSE}/join-requests").json() == []
    app.dependency_overrides.pop(require_teacher, None)

    app.dependency_overrides[require_student] = lambda: _student(
        student_uuid, other_teacher
    )
    app.dependency_overrides[require_principal] = lambda: Principal(
        kind=PrincipalKind.STUDENT, id=student_uuid
    )
    noop = client.post(
        "/courses/join-requests",
        json={"join_request": {"code": BASE_SIGNUP_CODE}},
    )
    assert noop.status_code == 200
    assert noop.json()["status"] == "already_enrolled"
    assert client.get("/courses/join-requests").json() == []
    student_courses = client.get("/courses")
    assert student_courses.status_code == 200
    for item in student_courses.json()["items"]:
        assert item.get("signup_code") is None
    app.dependency_overrides.pop(require_student, None)
    app.dependency_overrides.pop(require_principal, None)


def test_regenerate_signup_code(client: TestClient) -> None:
    app.dependency_overrides[require_teacher] = _seed_teacher
    before = client.get(f"/courses/{BASE_COURSE}").json()["signup_code"]
    regen = client.post(f"/course/{BASE_COURSE}/signup-code/regenerate")
    assert regen.status_code == 200
    after = regen.json()["signup_code"]
    assert after is not None
    assert len(after) == 4
    assert after != before
    app.dependency_overrides.pop(require_teacher, None)


def test_approve_single_join_request(
    client: TestClient, db_session: Session
) -> None:
    app.dependency_overrides[require_teacher] = _seed_teacher
    create_student = client.post(
        "/students",
        json={"username": "pending01", "password": "password123"},
    )
    assert create_student.status_code == 201
    student_uuid = create_student.json()["uuid"]
    app.dependency_overrides.pop(require_teacher, None)

    app.dependency_overrides[require_student] = lambda: _student(
        uuid.UUID(student_uuid), SEED_TEACHER_ID
    )
    req = client.post(
        "/courses/join-requests",
        json={"join_request": {"code": "EMPT"}},
    )
    assert req.status_code == 200
    assert req.json()["status"] == "pending"
    app.dependency_overrides.pop(require_student, None)

    empty_course = "0419df0c-080f-4a93-bb4e-82fc6121b073"
    app.dependency_overrides[require_teacher] = _seed_teacher
    approve = client.post(
        f"/course/{empty_course}/join-requests/approve",
        json={"enrollment": {"student_uuids": [student_uuid]}},
    )
    assert approve.status_code == 200
    assert approve.json()["enrolled"] == 1
    enrolled = client.get(f"/course/{empty_course}/students")
    assert any(s["uuid"] == student_uuid for s in enrolled.json())
    app.dependency_overrides.pop(require_teacher, None)
