def test_register(client):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "name": "Test User",
            "email": "register-test@example.com",
            "password": "password123",
        },
    )

    assert response.status_code == 201

    data = response.get_json()["data"]

    assert data["name"] == "Test User"
    assert data["email"] == "register-test@example.com"
    assert "password" not in data
    assert "password_hash" not in data


def test_login(client):
    client.post(
        "/api/v1/auth/register",
        json={
            "name": "Login User",
            "email": "login-test@example.com",
            "password": "password123",
        },
    )

    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "login-test@example.com",
            "password": "password123",
        },
    )

    assert response.status_code == 200

    data = response.get_json()["data"]

    assert data["access_token"]
    assert data["user"]["email"] == "login-test@example.com"


def test_login_with_invalid_password(client):
    client.post(
        "/api/v1/auth/register",
        json={
            "name": "Invalid Login",
            "email": "invalid-login@example.com",
            "password": "password123",
        },
    )

    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "invalid-login@example.com",
            "password": "wrong-password",
        },
    )

    assert response.status_code == 401


def test_protected_endpoint_requires_authentication(client):
    response = client.get("/api/v1/summary")

    assert response.status_code == 401
