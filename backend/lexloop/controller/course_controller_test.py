from fastapi.testclient import TestClient


def test_get_courses(client: TestClient) -> None:
    response = client.get("/courses")
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 2
    assert len(body["items"]) == 2
    assert body["items"][0]["name"] == "Base Course"
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
