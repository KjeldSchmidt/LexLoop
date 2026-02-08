from fastapi.testclient import TestClient


def test_get_courses(client: TestClient) -> None:
    response = client.get("/courses")
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["name"] == "Base Course"
