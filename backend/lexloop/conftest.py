from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from lexloop.repository import Base
from fastapi.testclient import TestClient

from .main import app
from lexloop.controller import get_db
from lexloop.auth import user_repository

import pytest
import asyncio


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

    user_repository._async_engine = None
    user_repository._async_sessionmaker = None

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    
    # Note: We don't override get_async_session because TestClient handles
    # async dependencies in its own event loop, and the async session will
    # naturally connect to the same test database
    
    yield TestClient(app)
    
    app.dependency_overrides.clear()
    
    # Clean up async engine after test if it was created
    if user_repository._async_engine is not None:
        try:
            asyncio.run(user_repository._async_engine.dispose())
        except:
            pass
        user_repository._async_engine = None
        user_repository._async_sessionmaker = None
