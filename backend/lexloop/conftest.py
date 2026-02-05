from pathlib import Path
from typing import Generator
from sqlalchemy import create_engine, Engine, text
from sqlalchemy.orm import sessionmaker, Session
from lexloop.repository.base import Base
from fastapi.testclient import TestClient

from .config import env_settings
from .main import app
from lexloop.controller import get_db
from lexloop.auth import user_manager

import pytest
import asyncio


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

    user_manager._async_engine = None
    user_manager._async_sessionmaker = None

    def override_get_db() -> Generator[Session, None, None]:
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)

    app.dependency_overrides.clear()

    # Clean up async engine after test if it was created. We never set this
    # explicitly, it gets it automatically from the TestClient context.
    if user_manager._async_engine is not None:
        asyncio.run(user_manager._async_engine.dispose())  # type: ignore[unreachable]
        user_manager._async_engine = None
        user_manager._async_sessionmaker = None
