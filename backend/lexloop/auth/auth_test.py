from fastapi.testclient import TestClient


def test_password_register_endpoint_is_disabled(client: TestClient) -> None:
    response = client.post(
        "/auth/register",
        json={
            "email": "test@lexloop.com",
            "password": "SECURE_PASSWORD",
        },
    )
    assert response.status_code == 404


def test_google_authorize_route_exists(client: TestClient) -> None:
    # Without real Google credentials this may 500 on exchange, but authorize
    # should at least be routed (redirect or error from OAuth client).
    response = client.get("/auth/google/authorize", follow_redirects=False)
    assert response.status_code in {200, 302, 400, 500}
