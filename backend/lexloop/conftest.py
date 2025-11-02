from typing import Generator

from fastapi.testclient import TestClient
from lexloop.repository import MetaBase

from .main import app
from .repository.ensure_tables import ensure_tables

import pytest
import boto3


@pytest.fixture(scope="session")
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_dynamodb() -> Generator[None, None, None]:
    dynamodb = boto3.client(
        "dynamodb",
        endpoint_url=MetaBase.host,
        region_name=MetaBase.region,
        aws_access_key_id="fake",
        aws_secret_access_key="fake",
    )

    tables = dynamodb.list_tables()["TableNames"]
    for name in tables:
        dynamodb.delete_table(TableName=name)

    ensure_tables()

    yield
