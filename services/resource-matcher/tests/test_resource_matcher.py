from fastapi.testclient import TestClient
from resource_matcher.main import app


def test_health() -> None:
    with TestClient(app) as client:
        assert client.get("/health/ready").json()["service"] == "resource-matcher"
