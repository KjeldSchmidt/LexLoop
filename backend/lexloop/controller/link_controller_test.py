from uuid import UUID

from fastapi.testclient import TestClient

from lexloop.model.link_model import LinkType


def test_add_link_returns_2xx(client: TestClient) -> None:
    node1_response = client.post(
        "/nodes", json={"term": "test1", "definition": "test", "synonyms": []}
    )

    node2_response = client.post(
        "/nodes", json={"term": "test2", "definition": "test", "synonyms": []}
    )

    response = client.post(
        "/links",
        json={
            "node1": node1_response.json()["uuid"],
            "node2": node2_response.json()["uuid"],
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
    node1_response = client.post(
        "/nodes", json={"term": "test1", "definition": "test", "synonyms": []}
    )

    node2_response = client.post(
        "/nodes", json={"term": "test2", "definition": "test", "synonyms": []}
    )
    response = client.post(
        "/links",
        json={
            "node1": node1_response.json()["uuid"],
            "node2": node2_response.json()["uuid"],
            "type": "SYNONYM",
            "annotation": "comment",
        },
    )
    assert response.status_code == 201

    response = client.get("/links")
    assert response.status_code == 200
    returned_link = response.json()[0]
    assert returned_link["node1"] == node1_response.json()["uuid"]
    assert returned_link["node2"] == node2_response.json()["uuid"]
    assert LinkType(returned_link["type"]) == LinkType.SYNONYM
    assert returned_link["annotation"] == "comment"
