from fastapi.testclient import TestClient


def test_add_node_returns_2xx(client: TestClient) -> None:
    response = client.post(
        "/nodes",
        json={
            "node": {
                "term": "test",
                "definition": "test",
                "tags": [],
                "course_uuid": "59cc5186-a10d-476e-b750-c8f5b821b953",
            },
        },
    )
    assert response.status_code == 201


def test_get_nodes_when_none_are_stored_returns_empty_list(
    client: TestClient,
) -> None:
    response = client.get("/course/0419df0c-080f-4a93-bb4e-82fc6121b073/nodes")
    assert response.status_code == 200
    assert response.json() == []


def test_get_nodes_when_nodes_are_added(client: TestClient) -> None:
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
    node_response = client.post(
        "/nodes",
        json={
            "node": {
                "term": "test",
                "definition": "test",
                "tags": [tag_response.json()["uuid"]],
                "course_uuid": "59cc5186-a10d-476e-b750-c8f5b821b953",
            }
        },
    )
    assert node_response.status_code == 201
    new_node_uuid = node_response.json()["uuid"]

    response = client.get("/course/59cc5186-a10d-476e-b750-c8f5b821b953/nodes")
    assert response.status_code == 200
    filtered_nodes = list(
        filter(lambda x: x["uuid"] == new_node_uuid, response.json())
    )
    assert len(filtered_nodes) == 1

    assert filtered_nodes[0]["term"] == "test"
    assert filtered_nodes[0]["definition"] == "test"
    assert (
        filtered_nodes[0]["course_uuid"]
        == "59cc5186-a10d-476e-b750-c8f5b821b953"
    )


def test_get_all_for_single_node(client: TestClient) -> None:
    example_node_uuid = "510a20c6-e818-44a5-a57b-a9e847f58950"
    expected_link_uuids = {
        "3456752f-d463-43ec-aa03-32837bca756c",
        "d4f814e8-497e-4c8a-8658-e53dea9c1109",
    }
    response = client.get(f"/nodes/{example_node_uuid}/links")
    assert response.status_code == 200
    data = response.json()
    actual_link_uuid_set = {link["uuid"] for link in data}
    assert actual_link_uuid_set == expected_link_uuids


def test_get_all_for_tags(client: TestClient) -> None:
    expected_node_uuids = {
        "510a20c6-e818-44a5-a57b-a9e847f58950",
        "55f04eba-3311-45be-a9e6-d8f14db3fa52",
        "7b17c724-a501-4b79-975e-23550464740d",
        "840d7d42-c26e-4f4f-abda-061181d504cd",
        "c24f126f-6a1f-4ff9-bf08-65488a179a3e",
        "c5a5fb3e-894d-4c0b-bbea-535a12f7ceff",
    }
    response = client.get("/nodes/tag/e0694e62-b746-4ed0-b24e-be1abb194eda")
    assert response.status_code == 200
    data = response.json()
    actual_node_uuids = {node["uuid"] for node in data}
    assert actual_node_uuids == expected_node_uuids


def test_add_tags_to_node(client: TestClient) -> None:
    tag_response = client.post(
        "/tags",
        json={
            "tag": {
                "title": "test_tag",
                "description": "test",
                "course_uuid": "0419df0c-080f-4a93-bb4e-82fc6121b073",
            }
        },
    )
    node_response = client.post(
        "/nodes",
        json={
            "node": {
                "term": "test",
                "definition": "test",
                "tags": [],
                "course_uuid": "0419df0c-080f-4a93-bb4e-82fc6121b073",
            },
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


def test_update_tags(client: TestClient) -> None:
    node_uuid = "b8e3cd0c-bee2-465a-a3cd-eb935212642c"
    tag_to_add_uuid = "910596b5-f15a-45be-a941-94c448539023"
    response = client.get(f"/nodes/{node_uuid}")
    tags = response.json()["tags"]
    assert len(tags) == 1

    response = client.post(
        f"/nodes/update/{node_uuid}/tags/",
        json={
            "tag_uuids": [
                tags[0],
                tag_to_add_uuid,
            ]
        },
    )
    assert response.status_code == 200
    assert len(response.json()["tags"]) == 2

    response = client.get(f"/nodes/{node_uuid}")
    tags = response.json()["tags"]
    assert len(tags) == 2
