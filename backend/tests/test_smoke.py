def test_app_starts(client):
    response = client.get("/health")

    assert response.status_code == 200
