import os

import pytest

from app import create_app
from app.extensions import db


from app.config.settings import Config


class TestConfig(Config):
    TESTING = True

    SECRET_KEY = "test-secret-key"
    JWT_SECRET_KEY = "test-jwt-secret-key-32-bytes-long"

    SQLALCHEMY_DATABASE_URI = (
        f"postgresql+psycopg://"
        f"{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}"
        f"/expense_tracker_test"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False


@pytest.fixture()
def app():
    app = create_app(TestConfig)

    with app.app_context():
        db.drop_all()
        db.create_all()

        yield app

        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def auth_client(client):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "password123",
        },
    )

    assert response.status_code == 201

    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "test@example.com",
            "password": "password123",
        },
    )

    assert response.status_code == 200

    token = response.get_json()["data"]["access_token"]

    client.environ_base["HTTP_AUTHORIZATION"] = f"Bearer {token}"

    return client

@pytest.fixture()
def category(auth_client):
    response = auth_client.post(
        "/api/v1/categories",
        json={
            "name": "Food",
            "type": "expense",
        },
    )

    assert response.status_code == 201

    return response.get_json()["data"]

@pytest.fixture()
def transaction(auth_client, category):
    response = auth_client.post(
        "/api/v1/transactions",
        json={
            "category_id": category["id"],
            "type": "expense",
            "amount": 100.00,
            "description": "Test transaction",
            "transaction_date": "2026-10-07",
        },
    )

    assert response.status_code == 201

    return response.get_json()["data"]
