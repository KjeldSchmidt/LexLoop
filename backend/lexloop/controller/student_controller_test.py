import uuid

from fastapi.testclient import TestClient
from pwdlib import PasswordHash
from sqlalchemy import text
from sqlalchemy.orm import Session

from lexloop.auth.principal import require_teacher
from lexloop.auth.user_model import User
from lexloop.main import app
from lexloop.repository.student_repository import StudentRepo

TEACHER_ID = uuid.UUID("a1111111-1111-4111-8111-111111111111")


def _teacher() -> User:
    return User(
        id=TEACHER_ID,
        email="teacher@lexloop.com",
        hashed_password="x",
        is_active=True,
        is_superuser=False,
        is_verified=True,
        role="teacher",
    )


def _ensure_teacher_row(db_session: Session) -> None:
    db_session.execute(
        text(
            """
            INSERT INTO "user"
              (id, email, hashed_password, is_active, is_superuser, is_verified, role)
            VALUES
              (
                'a1111111-1111-4111-8111-111111111111',
                'teacher@lexloop.com',
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
    db_session.commit()


def test_teacher_can_create_and_list_students(
    client: TestClient, db_session: Session
) -> None:
    _ensure_teacher_row(db_session)
    app.dependency_overrides[require_teacher] = _teacher

    create = client.post(
        "/students",
        json={"username": "pupil01", "password": "password123"},
    )
    assert create.status_code == 201
    assert create.json()["username"] == "pupil01"

    listed = client.get("/students")
    assert listed.status_code == 200
    assert any(s["username"] == "pupil01" for s in listed.json())

    app.dependency_overrides.pop(require_teacher, None)


def test_student_login_and_me(client: TestClient, db_session: Session) -> None:
    _ensure_teacher_row(db_session)
    hashed = PasswordHash.recommended().hash("password123")
    db_session.add(
        StudentRepo(
            uuid=uuid.uuid4(),
            username="pupil02",
            hashed_password=hashed,
            is_active=True,
            created_by_teacher_id=TEACHER_ID,
        )
    )
    db_session.commit()

    login = client.post(
        "/students/login",
        json={"username": "pupil02", "password": "password123"},
    )
    assert login.status_code == 200
    assert login.json()["username"] == "pupil02"
    assert "lexloop-studentauth" in login.cookies

    me = client.get("/students/me")
    assert me.status_code == 200
    assert me.json()["username"] == "pupil02"
