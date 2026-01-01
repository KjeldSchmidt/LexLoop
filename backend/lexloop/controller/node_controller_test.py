from uuid import UUID

from fastapi.testclient import TestClient


def test_add_node_returns_2xx(client: TestClient) -> None:
    response = client.post(
        "/nodes",
        json={"term": "test", "definition": "test", "tags": []},
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
    tag_response = client.post(
        "/tags",
        json={"title": "test_tag", "description": "test"},
    )
    response = client.post(
        "/nodes",
        json={
            "term": "test",
            "definition": "test",
            "tags": [tag_response.json()["uuid"]],
        },
    )
    assert response.status_code == 201

    response = client.get("/nodes")
    assert response.status_code == 200
    returned_node = response.json()[0]
    assert returned_node["term"] == "test"
    assert returned_node["definition"] == "test"


def test_get_all_for_single_node(client: TestClient) -> None:
    tag_response = client.post(
        "/tags",
        json={"title": "test_tag", "description": "test"},
    )
    tag2_response = client.post(
        "/tags",
        json={"title": "test_tag2", "description": "test"},
    )
    node1_response = client.post(
        "/nodes",
        json={"term": "test1", "definition": "test", "tags": []},
    )

    node2_response = client.post(
        "/nodes",
        json={
            "term": "test2",
            "definition": "test",
            "tags": [tag_response.json()["uuid"], tag2_response.json()["uuid"]],
        },
    )

    node3_response = client.post(
        "/nodes",
        json={
            "term": "test3",
            "definition": "test",
            "tags": [tag_response.json()["uuid"]],
        },
    )

    link1_response = client.post(
        "/links",
        json={
            "node1": node1_response.json()["uuid"],
            "node2": node2_response.json()["uuid"],
            "type": "SYNONYM",
            "annotation": "comment",
        },
    )

    link2_response = client.post(
        "/links",
        json={
            "node1": node3_response.json()["uuid"],
            "node2": node1_response.json()["uuid"],
            "type": "SYNONYM",
            "annotation": "comment",
        },
    )

    client.post(
        "/links",
        json={
            "node1": node2_response.json()["uuid"],
            "node2": node3_response.json()["uuid"],
            "type": "SYNONYM",
            "annotation": "comment",
        },
    )

    response = client.get(f"/nodes/{node1_response.json()['uuid']}/links")
    assert response.status_code == 200
    data = response.json()
    uuid_set = {link["uuid"] for link in data}
    assert link1_response.json()["uuid"] in uuid_set
    assert link2_response.json()["uuid"] in uuid_set
    assert len(data) == 2


def test_get_all_for_tags(client: TestClient) -> None:
    tag1_response = client.post(
        "/tags",
        json={"title": "test_tag", "description": "test"},
    )
    tag2_response = client.post(
        "/tags",
        json={"title": "test_tag2", "description": "test"},
    )
    client.post(
        "/nodes",
        json={"term": "test1", "definition": "test", "tags": []},
    )

    node2_response = client.post(
        "/nodes",
        json={
            "term": "test2",
            "definition": "test",
            "tags": [
                tag1_response.json()["uuid"],
                tag2_response.json()["uuid"],
            ],
        },
    )

    node3_response = client.post(
        "/nodes",
        json={
            "term": "test3",
            "definition": "test",
            "tags": [tag1_response.json()["uuid"]],
        },
    )

    response = client.get(f"/nodes/tag/{tag1_response.json()['uuid']}")
    assert response.status_code == 200
    data = response.json()
    uuid_set = {node["uuid"] for node in data}
    assert node2_response.json()["uuid"] in uuid_set
    assert node3_response.json()["uuid"] in uuid_set
    assert len(data) == 2

    response = client.get(f"/nodes/tag/{tag2_response.json()['uuid']}")
    assert response.status_code == 200
    data = response.json()
    uuid_set = {node["uuid"] for node in data}
    assert node2_response.json()["uuid"] in uuid_set
    assert len(data) == 1


def test_add_tags_to_node(client: TestClient) -> None:
    tag_response = client.post(
        "/tags",
        json={"title": "test_tag", "description": "test"},
    )
    node_response = client.post(
        "/nodes",
        json={
            "term": "test",
            "definition": "test",
            "tags": [],
        },
    )
    assert len(node_response.json()["tags"]) == 0

    response = client.post(
        f"/nodes/{node_response.json()['uuid']}/{tag_response.json()['uuid']}"
    )
    assert response.status_code == 200

    returned_node = response.json()
    assert len(returned_node["tags"]) == 1

    response = client.get(f"/tags/node/{node_response.json()['uuid']}")
    assert response.status_code == 200
    assert len(response.json()) == 1
