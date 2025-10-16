from uuid import UUID

from fastapi.testclient import TestClient

from lexloop.model.link_model import LinkType


def test_add_link_returns_2xx(client: TestClient) -> None:
    response = client.post(
        "/links",
        json={
            "word1": "test",
            "word2": "test2",
            "type": "SYNONYM",
            "annotation": "comment",
        },
    )
    assert response.status_code == 201
    data = response.json()
    UUID(data["uuid"])


def test_get_links_when_none_are_stored_returns_empty_list(
    client: TestClient,
) -> None:
    response = client.get("/links")
    assert response.status_code == 200
    assert response.json() == []


def test_get_links_when_links_are_added(client: TestClient) -> None:
    response = client.post(
        "/links",
        json={
            "word1": "test",
            "word2": "test2",
            "type": "SYNONYM",
            "annotation": "comment",
        },
    )
    assert response.status_code == 201

    response = client.get("/links")
    assert response.status_code == 200
    returned_link = response.json()[0]
    assert returned_link["word1"] == "test"
    assert returned_link["word2"] == "test2"
    assert LinkType(returned_link["type"]) == LinkType.SYNONYM
    assert returned_link["annotation"] == "comment"
