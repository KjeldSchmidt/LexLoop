from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from lexloop.repository import Base
from fastapi.testclient import TestClient

from .main import app
from lexloop.controller import get_db

import pytest


@pytest.fixture(scope="session")
def engine():
    return create_engine("postgresql://user:password@localhost:5435/lexloopdb")


@pytest.fixture(scope="session")
def tables(engine):
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture
def db_session(engine, tables):
    """Provide a transactional scope for each test"""
    connection = engine.connect()
    transaction = connection.begin()
    session = sessionmaker(bind=connection)(autoflush=False, autocommit=False)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(engine, tables, db_session):
    """Provide a test client with overridden database dependency"""

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()
