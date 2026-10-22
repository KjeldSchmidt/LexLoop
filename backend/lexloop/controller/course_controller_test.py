import uuid

from fastapi.testclient import TestClient
from sqlalchemy import text
from sqlalchemy.orm import Session

from lexloop.auth.principal import require_teacher
from lexloop.auth.user_model import User
from lexloop.main import app

SEED_TEACHER_ID = uuid.UUID("11111111-1111-4111-8111-111111111111")
BASE_COURSE = "59cc5186-a10d-476e-b750-c8f5b821b953"


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


def test_get_courses(client: TestClient) -> None:
    response = client.get("/courses")
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 2
    assert len(body["items"]) == 2
    assert body["items"][0]["name"] == "Base Course"
    assert body["items"][0]["description"] == "Seed vocabulary course"
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
