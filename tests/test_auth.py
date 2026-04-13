from tests.conftest import client


def test_signup():
    response = client.post(
        "/users/signup",
        json={
            "username": "ibrahim",
            "email": "ibrahim@example.com",
            "password": "testpassword123",
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "ibrahim"
    assert data["email"] == "ibrahim@example.com"
    assert data["role"] == "learner"


def test_login():
    client.post(
        "/users/signup",
        json={
            "username": "ibrahim",
            "email": "ibrahim@example.com",
            "password": "testpassword123",
        },
    )

    response = client.post(
        "/users/login",
        json={
            "email": "ibrahim@example.com",
            "password": "testpassword123",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_get_current_user():
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

    response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "ibrahim@example.com"
