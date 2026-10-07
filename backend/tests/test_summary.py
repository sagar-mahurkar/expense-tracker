def test_overall_summary(auth_client, category):
    auth_client.post(
        "/api/v1/transactions",
        json={
            "category_id": category["id"],
            "type": "expense",
            "amount": 100.00,
            "description": "Expense",
            "transaction_date": "2026-10-07",
        },
    )

    response = auth_client.get("/api/v1/summary")

    assert response.status_code == 200
    data = response.get_json()["data"]
    
    assert data["income"] == "0"
    assert data["expense"] == "100.00"
    assert data["balance"] == "-100.00"


def test_monthly_summary(auth_client, category):
    auth_client.post(
        "/api/v1/transactions",
        json={
            "category_id": category["id"],
            "type": "expense",
            "amount": 100.00,
            "description": "October expense",
            "transaction_date": "2026-10-07",
        },
    )

    response = auth_client.get(
        "/api/v1/summary/monthly?year=2026&month=10"
    )

    assert response.status_code == 200
    data = response.get_json()["data"]
    
    assert data["income"] == "0"
    assert data["expense"] == "100.00"
    assert data["balance"] == "-100.00"


def test_monthly_summary_empty_month(auth_client):
    response = auth_client.get(
        "/api/v1/summary/monthly?year=2026&month=1"
    )

    assert response.status_code == 200
    data = response.get_json()["data"]

    assert data["income"] == "0"
    assert data["expense"] == "0"
    assert data["balance"] == "0"


def test_monthly_summary_invalid_month(auth_client):
    response = auth_client.get(
        "/api/v1/summary/monthly?year=2026&month=13"
    )

    assert response.status_code == 400


def test_monthly_summary_missing_parameters(auth_client):
    response = auth_client.get("/api/v1/summary/monthly")

    assert response.status_code == 400
