from uuid import UUID

from fastapi.testclient import TestClient


def test_add_tag_returns_2xx(client: TestClient) -> None:
    response = client.post(
        "/tags",
        json={"title": "test_tag", "description": "test"},
    )

    assert response.status_code == 201
    data = response.json()
    UUID(data["uuid"])


def test_get_tags_when_none_are_stored_returns_empty_list(
    client: TestClient,
) -> None:
    response = client.get("/tags")
    assert response.status_code == 200
    assert response.json() == []


def test_get_tag_by_uuid(client: TestClient) -> None:
    tag_response = client.post(
        "/tags",
        json={"title": "test_tag", "description": "test"},
    )
    assert tag_response.status_code == 201

    response = client.get(f"/tags/{tag_response.json()['uuid']}")
    assert response.status_code == 200
    returned_tag = response.json()
    assert returned_tag["title"] == "test_tag"
    assert returned_tag["description"] == "test"


def test_get_tags_when_tags_are_added(client: TestClient) -> None:
    tag1_response = client.post(
        "/tags",
        json={"title": "test_tag", "description": "test"},
    )
    assert tag1_response.status_code == 201

    response = client.get("/tags")
    assert response.status_code == 200
    assert len(response.json()) == 1
    returned_tag = response.json()[0]
    assert returned_tag["title"] == "test_tag"
    assert returned_tag["description"] == "test"
