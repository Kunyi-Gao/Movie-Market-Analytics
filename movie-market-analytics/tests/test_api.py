from src.api.app import create_app


def test_health_check():
    app = create_app()
    client = app.test_client()
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.get_json()["success"] is True


def test_404_returns_json():
    app = create_app()
    client = app.test_client()
    response = client.get("/api/v1/nonexistent")
    assert response.status_code == 404
    assert response.is_json
    assert response.get_json()["success"] is False
