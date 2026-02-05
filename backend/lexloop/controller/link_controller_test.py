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
                "course_uuid": "59cc5186-a10d-476e-b750-c8f5b821b953",
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
                "course_uuid": "59cc5186-a10d-476e-b750-c8f5b821b953",
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
    response = client.get("/course/0419df0c-080f-4a93-bb4e-82fc6121b073/links")
    assert response.status_code == 200
    assert response.json() == []


def test_get_links_when_links_are_added(client: TestClient) -> None:
    node1_response = client.post(
        "/nodes",
        json={
            "node": {
                "term": "test1",
                "definition": "test",
                "tags": [],
                "course_uuid": "59cc5186-a10d-476e-b750-c8f5b821b953",
            },
        },
    )

    node2_response = client.post(
        "/nodes",
        json={
            "node": {
                "term": "test2",
                "definition": "test",
                "tags": [],
                "course_uuid": "59cc5186-a10d-476e-b750-c8f5b821b953",
            },
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

    response = client.get("/course/59cc5186-a10d-476e-b750-c8f5b821b953/links")
    assert response.status_code == 200

    print(response.json())
    filtered_links = list(
        filter(
            lambda x: x["node1"] == node1_response.json()["uuid"]
            and x["node2"] == node2_response.json()["uuid"],
            response.json(),
        )
    )
    assert len(filtered_links) == 1

    returned_link = filtered_links[0]
    assert returned_link["node1"] == node1_response.json()["uuid"]
    assert returned_link["node2"] == node2_response.json()["uuid"]
    assert LinkType(returned_link["type"]) == LinkType.SYNONYM
    assert returned_link["annotation"] == "comment"


def test_get_link_types(client: TestClient) -> None:
    response = client.get("/links/types")
    assert response.status_code == 200
    assert len(response.json()) == 5
    assert response.json()[0]["value"] == "SYNONYM"
