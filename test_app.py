import pytest
from fastapi.testclient import TestClient
from main import app, data

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_data():
    data.clear()
    yield
    data.clear()


def test_create_user():
    response = client.post(
        "/users",
        params={"name": "Hiral", "age": 25}
    )

    assert response.status_code == 200
    assert response.json() == {
        "user_id": 1,
        "name": "Hiral",
        "age": 25
    }


def test_get_existing_user():
    client.post(
        "/users",
        params={"name": "Hiral", "age": 25}
    )

    response = client.get("/users/1")

    assert response.status_code == 200
    assert response.json() == {
        "name": "Hiral",
        "age": 25
    }


def test_get_non_existing_user():
    response = client.get("/users/999")

    assert response.status_code == 200
    assert response.json() == {
        "message": "User not found"
    }


def test_delete_existing_user():
    client.post(
        "/users",
        params={"name": "Hiral", "age": 25}
    )

    response = client.delete("/users/1")

    assert response.status_code == 200
    assert response.json() == {
        "message": "User 1 deleted successfully"
    }


def test_delete_non_existing_user():
    response = client.delete("/users/999")

    assert response.status_code == 200
    assert response.json() == {
        "message": "User not found"
    }


def test_user_removed_after_delete():
    client.post(
        "/users",
        params={"name": "Hiral", "age": 25}
    )

    client.delete("/users/1")

    response = client.get("/users/1")

    assert response.status_code == 200
    assert response.json() == {
        "message": "User not found"
    }