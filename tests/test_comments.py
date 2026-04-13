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

    return login_response.json()["access_token"]


def create_discussion(token):
    response = client.post(
        "/discussions/",
        json={
            "title": "Discussion title",
            "content": "Discussion content",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    return response.json()["id"]


def test_create_comment():
    token = create_user_and_token()
    discussion_id = create_discussion(token)

    response = client.post(
        f"/comments/discussion/{discussion_id}",
        json={"content": "My first comment"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 201
    data = response.json()
    assert data["content"] == "My first comment"
    assert data["discussion_id"] == discussion_id


def test_get_comments_for_discussion():
    token = create_user_and_token()
    discussion_id = create_discussion(token)

    client.post(
        f"/comments/discussion/{discussion_id}",
        json={"content": "My first comment"},
        headers={"Authorization": f"Bearer {token}"},
    )

    response = client.get(
        f"/comments/discussion/{discussion_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 1
