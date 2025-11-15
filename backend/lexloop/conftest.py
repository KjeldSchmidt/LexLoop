from typing import Generator
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session
from lexloop.repository.base import Base
from fastapi.testclient import TestClient

from .main import app
from lexloop.controller import get_db
from lexloop.auth import user_repository

import pytest
import asyncio


@pytest.fixture(scope="session")
def engine() -> Engine:
    return create_engine("postgresql://user:password@localhost:5435/lexloopdb")


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

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(
    engine: Engine, tables: object, db_session: Session
) -> Generator[TestClient, None, None]:
    """Provide a test client with overridden database dependency"""

    user_repository._async_engine = None
    user_repository._async_sessionmaker = None

    def override_get_db() -> Generator[Session, None, None]:
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)

    app.dependency_overrides.clear()

    # Clean up async engine after test if it was created. We never set this
    # explicitly, it gets it automatically from the TestClient context.
    if user_repository._async_engine is not None:
        asyncio.run(user_repository._async_engine.dispose())  # type: ignore[unreachable]
        user_repository._async_engine = None
        user_repository._async_sessionmaker = None
