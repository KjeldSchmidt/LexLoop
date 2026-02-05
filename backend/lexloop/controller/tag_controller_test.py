from uuid import UUID

from fastapi.testclient import TestClient


def test_add_tag_returns_2xx(client: TestClient) -> None:
    response = client.post(
        "/tags",
        json={
            "tag": {
                "title": "test_tag",
                "description": "test",
                "course_uuid": "59cc5186-a10d-476e-b750-c8f5b821b953",
            }
        },
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
        json={
            "tag": {
                "title": "test_tag",
                "description": "test",
                "course_uuid": "59cc5186-a10d-476e-b750-c8f5b821b953",
            }
        },
    )
    assert tag_response.status_code == 201

    response = client.get(f"/tags/{tag_response.json()['uuid']}")
    assert response.status_code == 200
    returned_tag = response.json()
    assert returned_tag["title"] == "test_tag"
    assert returned_tag["description"] == "test"


def test_get_tags_when_tags_are_added(client: TestClient) -> None:
    tag_response = client.post(
        "/tags",
        json={
            "tag": {
                "title": "test_tag",
                "description": "test",
                "course_uuid": "59cc5186-a10d-476e-b750-c8f5b821b953",
            }
        },
    )
    assert tag_response.status_code == 201
    new_tag_uuid = tag_response.json()["uuid"]

    response = client.get("/course/59cc5186-a10d-476e-b750-c8f5b821b953/tags")
    assert response.status_code == 200
    filtered_tags = list(
        filter(lambda x: x["uuid"] == new_tag_uuid, response.json())
    )
    assert len(filtered_tags) == 1

    returned_tag = filtered_tags[0]
    assert returned_tag["title"] == "test_tag"
    assert returned_tag["description"] == "test"


def test_get_tags_for_node(client: TestClient) -> None:
    tag1_response = client.post(
        "/tags",
        json={"tag": {"title": "test_tag", "description": "test"}},
    )
    tag2_response = client.post(
        "/tags",
        json={"tag": {"title": "test_tag2", "description": "test2"}},
    )
    node_response = client.post(
        "/nodes",
        json={
            "node": {
                "term": "test_node",
                "definition": "test_definition",
                "tags": [
                    tag1_response.json()["uuid"],
                    tag2_response.json()["uuid"],
                ],
            },
        },
    )
    assert tag1_response.status_code == 201
    assert tag2_response.status_code == 201
    assert node_response.status_code == 201

    response = client.get(f"/tags/node/{node_response.json()['uuid']}")
    assert response.status_code == 200
    assert len(response.json()) == 2
    returned_tag1 = response.json()[0]
    assert returned_tag1["title"] == "test_tag"
    assert returned_tag1["description"] == "test"
    returned_tag2 = response.json()[1]
    assert returned_tag2["title"] == "test_tag2"
    assert returned_tag2["description"] == "test2"
