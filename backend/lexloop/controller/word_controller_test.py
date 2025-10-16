from uuid import UUID

from fastapi.testclient import TestClient


def test_add_word_returns_2xx(client: TestClient) -> None:
    response = client.post(
        "/words", json={"word": "test", "definition": "test", "synonyms": []}
    )
    assert response.status_code == 201
    data = response.json()
    UUID(data["uuid"])


def test_get_words_when_none_are_stored_returns_empty_list(
    client: TestClient,
) -> None:
    response = client.get("/words")
    assert response.status_code == 200
    assert response.json() == []


def test_get_words_when_words_are_added(client: TestClient) -> None:
    response = client.post(
        "/words", json={"word": "test", "definition": "test", "synonyms": []}
    )
    assert response.status_code == 201

    response = client.get("/words")
    assert response.status_code == 200
    returned_word = response.json()[0]
    assert returned_word["word"] == "test"
    assert returned_word["definition"] == "test"


def test_synomyms_are_saved_on_creation(client: TestClient) -> None:
    response = client.post(
        "/words", json={"word": "test", "definition": "test", "synonyms": []}
    )
    assert response.status_code == 201
    first_word_uuid = response.json()["uuid"]
    response = client.post(
        "/words",
        json={
            "word": "test2",
            "definition": "test2",
            "synonyms": [first_word_uuid],
        },
    )

    second_word_retrieved = client.get(
        f"/words/{response.json()['uuid']}"
    ).json()
    assert second_word_retrieved["synonyms"] == [first_word_uuid]
