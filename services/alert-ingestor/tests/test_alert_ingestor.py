from alert_ingestor.main import app
from fastapi.testclient import TestClient


def test_health_and_mock_provider() -> None:
    with TestClient(app) as client:
        assert client.get("/health/live").status_code == 200
        response = client.get("/api/v1/demo/alerts")
        assert response.status_code == 200
        assert response.json()[0]["provider_id"] == "mock-weather-001"
