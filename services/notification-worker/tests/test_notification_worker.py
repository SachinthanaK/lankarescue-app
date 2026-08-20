from fastapi.testclient import TestClient
from notification_worker.main import app


def test_health() -> None:
    with TestClient(app) as client:
        assert client.get("/meta").json()["service"] == "notification-worker"
