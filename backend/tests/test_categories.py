def test_create_category(auth_client):
    response = auth_client.post(
        "/api/v1/categories",
        json={
            "name": "Salary",
            "type": "income",
        },
    )

    assert response.status_code == 201
    data = response.get_json()["data"]
    assert data["name"] == "Salary"
    assert data["type"] == "income"


def test_list_categories(auth_client, category):
    response = auth_client.get("/api/v1/categories")

    assert response.status_code == 200
    data = response.get_json()["data"]
    assert len(data) == 1
    assert data[0]["id"] == category["id"]


def test_get_category(auth_client, category):
    response = auth_client.get(
        f"/api/v1/categories/{category['id']}"
    )

    assert response.status_code == 200
    data = response.get_json()["data"]
    assert data["id"] == category["id"]


def test_delete_category(auth_client, category):
    response = auth_client.delete(
        f"/api/v1/categories/{category['id']}"
    )

    assert response.status_code == 204

    response = auth_client.get(
        f"/api/v1/categories/{category['id']}"
    )
    assert response.status_code == 404
