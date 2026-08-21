from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


def test_register_user():

    response = client.post(
        "/auth/register",
        json={
            "username": "auth_test_user",
            "email": "auth_test@example.com",
            "password": "TestPass123",
            "role": "user"
        }
    )

    assert response.status_code in [200, 400]


def test_login_user():

    response = client.post(
        "/auth/login",
        data={
            "username": "auth_test_user",
            "password": "TestPass123"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password():

    response = client.post(
        "/auth/login",
        data={
            "username": "auth_test_user",
            "password": "WrongPassword123"
        }
    )

    assert response.status_code == 401