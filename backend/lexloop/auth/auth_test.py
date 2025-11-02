from fastapi.testclient import TestClient


def test_can_register_new_user_but_not_log_in_without_verification(
    client: TestClient,
) -> None:
    login_details = {
        "username": "test@lexloop.com",
        "password": "SECURE_PASSWORD",
    }
    register_details = {
        "email": "test@lexloop.com",
        "password": "SECURE_PASSWORD",
    }

    first_login_attempt = client.post("/auth/login", data=login_details)
    assert first_login_attempt.json()["detail"] == "LOGIN_BAD_CREDENTIALS"

    response = client.post("/auth/register", json=register_details)

    assert response.status_code == 201

    second_login_attempt = client.post("/auth/login", data=login_details)
    assert second_login_attempt.json()["detail"] == "LOGIN_USER_NOT_VERIFIED"
