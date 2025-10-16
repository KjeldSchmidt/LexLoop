from uuid import UUID

from fastapi.testclient import TestClient


def test_add_node_returns_2xx(client: TestClient) -> None:
    response = client.post(
        "/nodes", json={"term": "test", "definition": "test"}
    )
    assert response.status_code == 201
    data = response.json()
    UUID(data["uuid"])


def test_get_nodes_when_none_are_stored_returns_empty_list(
    client: TestClient,
) -> None:
    response = client.get("/nodes")
    assert response.status_code == 200
    assert response.json() == []


def test_get_nodes_when_nodes_are_added(client: TestClient) -> None:
    response = client.post(
        "/nodes", json={"term": "test", "definition": "test"}
    )
    assert response.status_code == 201

    response = client.get("/nodes")
    assert response.status_code == 200
    returned_node = response.json()[0]
    assert returned_node["term"] == "test"
    assert returned_node["definition"] == "test"
