import pytest
import random
import string


@pytest.fixture
def user_data():
    return {
        "name": "".join(
            random.choice(string.ascii_letters)
            for _ in range(8)
        ),
        "age": random.randint(18, 80)
    }

from fastapi.testclient import TestClient
from main_app import app, data

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_data():
    data.clear()


def test_create_user(user_data):
    response = client.post(
        "/users",
        params=user_data
    )

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["name"] == user_data["name"]
    assert response_data["age"] == user_data["age"]
    assert response_data["user_id"] == 1


def test_get_users(user_data):
    client.post("/users", params=user_data)

    response = client.get("/users")

    assert response.status_code == 200

    users = response.json()

    assert len(users) == 1


def test_delete_user(user_data):
    create_response = client.post(
        "/users",
        params=user_data
    )

    user_id = create_response.json()["user_id"]

    delete_response = client.delete(
        f"/users/{user_id}"
    )

    assert delete_response.status_code == 200
    assert (
        delete_response.json()["message"]
        == f"User {user_id} deleted successfully"
    )


