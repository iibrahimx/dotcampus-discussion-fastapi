from tests.conftest import client


def create_user_and_token():
    client.post(
        "/users/signup",
        json={
            "username": "ibrahim",
            "email": "ibrahim@example.com",
            "password": "testpassword123",
        },
    )

    login_response = client.post(
        "/users/login",
        json={
            "email": "ibrahim@example.com",
            "password": "testpassword123",
        },
    )

    token = login_response.json()["access_token"]
    return token


def test_create_discussion():
    token = create_user_and_token()

    response = client.post(
        "/discussions/",
        json={
            "title": "My first discussion",
            "content": "This is my first discussion post.",
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "My first discussion"
    assert data["owner_id"] == 1


def test_get_all_discussions():
    token = create_user_and_token()

    client.post(
        "/discussions/",
        json={
            "title": "My first discussion",
            "content": "This is my first discussion post.",
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    response = client.get(
        "/discussions/",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 1
