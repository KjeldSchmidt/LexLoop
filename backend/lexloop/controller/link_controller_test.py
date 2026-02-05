import uuid
from uuid import UUID

from fastapi.testclient import TestClient

from lexloop.model.link_model import LinkType


def test_add_link_returns_2xx(client: TestClient) -> None:
    node1_response = client.post(
        "/nodes",
        json={
            "node": {
                "term": "test1",
                "definition": "test",
                "tags": [],
                "course_uuid": "44abe87e-02cc-11f1-bf14-00155d0892d6",
            }
        },
    )

    node2_response = client.post(
        "/nodes",
        json={
            "node": {
                "term": "test2",
                "definition": "test",
                "tags": [],
                "course_uuid": "44abe87e-02cc-11f1-bf14-00155d0892d6",
            }
        },
    )

    response = client.post(
        "/links",
        json={
            "link": {
                "node1": node1_response.json()["uuid"],
                "node2": node2_response.json()["uuid"],
                "type": "SYNONYM",
                "annotation": "comment",
            }
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
        "/nodes",
        json={
            "node": {"term": "test1", "definition": "test", "tags": []},
        },
    )

    node2_response = client.post(
        "/nodes",
        json={
            "node": {"term": "test2", "definition": "test", "tags": []},
        },
    )
    response = client.post(
        "/links",
        json={
            "link": {
                "node1": node1_response.json()["uuid"],
                "node2": node2_response.json()["uuid"],
                "type": "SYNONYM",
                "annotation": "comment",
            }
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


def test_get_link_types(client: TestClient) -> None:
    response = client.get("/links/types")
    assert response.status_code == 200
    assert len(response.json()) == 5
    assert response.json()[0]["value"] == "SYNONYM"
