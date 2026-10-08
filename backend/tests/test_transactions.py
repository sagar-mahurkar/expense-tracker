def test_create_transaction(auth_client, category):
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

    data = response.get_json()["data"]

    assert data["amount"] == "100.00"
    assert data["type"] == "expense"
    assert data["category_id"] == category["id"]


def test_get_transaction(auth_client, transaction):
    response = auth_client.get(
        f"/api/v1/transactions/{transaction['id']}"
    )

    assert response.status_code == 200

    data = response.get_json()["data"]

    assert data["id"] == transaction["id"]


def test_update_transaction(auth_client, transaction, category):
    response = auth_client.put(
        f"/api/v1/transactions/{transaction['id']}",
        json={
            "category_id": category["id"],
            "type": "expense",
            "amount": 150.00,
            "description": "Updated transaction",
            "transaction_date": "2026-10-07",
        },
    )

    assert response.status_code == 200

    data = response.get_json()["data"]

    assert data["amount"] == "150.00"
    assert data["description"] == "Updated transaction"


def test_list_transactions(auth_client, transaction):
    response = auth_client.get("/api/v1/transactions")

    assert response.status_code == 200

    data = response.get_json()

    assert data["pagination"]["total"] == 1
    assert len(data["data"]) == 1


def test_transaction_type_filter(auth_client, transaction):
    response = auth_client.get(
        "/api/v1/transactions?type=expense"
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["pagination"]["total"] == 1


def test_transaction_search(auth_client, transaction):
    response = auth_client.get(
        "/api/v1/transactions?search=Test%20transaction"
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["pagination"]["total"] == 1


def test_transaction_search_by_category(
    auth_client,
    transaction,
):
    response = auth_client.get(
        "/api/v1/transactions?search=Food"
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["pagination"]["total"] == 1

def test_transaction_date_filter(auth_client, transaction):
    response = auth_client.get(
        "/api/v1/transactions"
        "?start_date=2026-10-07&end_date=2026-10-07"
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["pagination"]["total"] == 1


def test_transaction_pagination(auth_client, transaction):
    response = auth_client.get(
        "/api/v1/transactions?page=1&per_page=1"
    )

    assert response.status_code == 200

    pagination = response.get_json()["pagination"]

    assert pagination["page"] == 1
    assert pagination["per_page"] == 1
    assert pagination["total"] == 1
    assert pagination["total_pages"] == 1


def test_delete_transaction(auth_client, transaction):
    response = auth_client.delete(
        f"/api/v1/transactions/{transaction['id']}"
    )

    assert response.status_code == 204

    response = auth_client.get(
        f"/api/v1/transactions/{transaction['id']}"
    )

    assert response.status_code == 404

def test_transaction_user_isolation(auth_client, category, transaction, client):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "name": "Other User",
            "email": "other@example.com",
            "password": "password123",
        },
    )
    assert response.status_code == 201

    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "other@example.com",
            "password": "password123",
        },
    )
    assert response.status_code == 200

    token = response.get_json()["data"]["access_token"]
    client.environ_base["HTTP_AUTHORIZATION"] = f"Bearer {token}"

    response = client.get(
        f"/api/v1/transactions/{transaction['id']}"
    )

    assert response.status_code == 404

