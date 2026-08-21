import os

os.environ["DB_NAME"] = "employee_management_test"

import pytest
from fastapi.testclient import TestClient

from main import app
from database import users_collection


@pytest.fixture
def client():

    # Remove old test user so its role is reset
    users_collection.delete_one({
        "username": "pytest_user"
    })

    test_client = TestClient(app)

    # Create admin test user
    response = test_client.post(
        "/auth/register",
        json={
            "username": "pytest_user",
            "email": "pytest@example.com",
            "password": "TestPass123",
            "role": "admin"
        }
    )

    assert response.status_code == 200

    # Login using OAuth2 form data
    login_response = test_client.post(
        "/auth/login",
        data={
            "username": "pytest_user",
            "password": "TestPass123"
        }
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    # Automatically authenticate all test requests
    test_client.headers.update({
        "Authorization": f"Bearer {token}"
    })

    yield test_client