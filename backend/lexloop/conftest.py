import asyncio
import uuid
from pathlib import Path
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import Engine, create_engine, text
from sqlalchemy.orm import Session, sessionmaker

# Import models so Base.metadata.create_all sees all tables.
import lexloop.auth.user_repository  # noqa: F401
import lexloop.repository.course_repository  # noqa: F401
import lexloop.repository.link_repository  # noqa: F401
import lexloop.repository.node_repository  # noqa: F401
import lexloop.repository.student_repository  # noqa: F401
import lexloop.repository.tag_repository  # noqa: F401
from lexloop.auth import user_manager
from lexloop.auth.principal import Principal, PrincipalKind, require_principal
from lexloop.config import env_settings
from lexloop.controller import get_db
from lexloop.main import app
from lexloop.repository.base import Base


@pytest.fixture(scope="session")
def engine() -> Engine:
    return create_engine(env_settings.DB_URL)


@pytest.fixture(scope="session")
def tables(engine: Engine) -> Generator[None, None, None]:
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture
def db_session(
    engine: Engine, tables: object
) -> Generator[Session, None, None]:
    """Provide a transactional scope for each test"""
    connection = engine.connect()
    transaction = connection.begin()
    session = sessionmaker(bind=connection)(autoflush=False, autocommit=False)

    seed_path = Path(__file__).parent.parent / "db_seed.sql"
    seed_command = seed_path.read_text()
    session.execute(text(seed_command))

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(
    engine: Engine, tables: object, db_session: Session
) -> Generator[TestClient, None, None]:
    """Provide a test client with overridden database dependency"""

    user_manager.reset_async_engine_for_tests()

    def override_get_db() -> Generator[Session, None, None]:
        yield db_session

    def override_principal() -> Principal:
        # Matches seed teacher in db_seed.sql (owns Base Course / Empty Course).
        return Principal(
            kind=PrincipalKind.TEACHER,
            id=uuid.UUID("11111111-1111-4111-8111-111111111111"),
        )

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[require_principal] = override_principal

    yield TestClient(app)

    app.dependency_overrides.clear()

    # Clean up async engine after test if it was created during the request.
    asyncio.run(user_manager.dispose_async_engine())
