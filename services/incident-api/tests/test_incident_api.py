from fastapi.testclient import TestClient
from incident_api.main import app


def payload() -> dict[str, object]:
    return {
        "district": "Colombo",
        "location": "Colombo Fort railway station",
        "needType": "water",
        "peopleCount": 12,
        "priority": "urgent",
        "description": "Clean drinking water is needed for displaced families.",
        "contactMethod": "phone",
        "contactValue": "+94 77 123 4567",
    }


def test_health_and_metadata() -> None:
    with TestClient(app) as client:
        assert client.get("/health/live").json()["status"] == "ok"
        assert client.get("/health/ready").json()["status"] == "ready"
        assert client.get("/meta").json()["service"] == "incident-api"


def test_create_track_and_demo_queue() -> None:
    with TestClient(app) as client:
        created = client.post("/api/v1/relief-requests", json=payload())
        assert created.status_code == 201
        secret = created.json()
        assert secret["reference"].startswith("REQ-")
        assert len(secret["trackingToken"]) >= 32

        tracked = client.post(
            "/api/v1/relief-requests/track",
            json={"reference": secret["reference"], "trackingToken": secret["trackingToken"]},
        )
        assert tracked.status_code == 200
        assert tracked.json()["status"] == "submitted"
        assert "contactValue" not in tracked.json()

        queue = client.get("/api/v1/demo/staff/relief-requests")
        assert queue.status_code == 200
        assert queue.json()[0]["reference"] == secret["reference"]


def test_wrong_tracking_token_does_not_reveal_request() -> None:
    with TestClient(app) as client:
        created = client.post("/api/v1/relief-requests", json=payload()).json()
        response = client.post(
            "/api/v1/relief-requests/track",
            json={"reference": created["reference"], "trackingToken": "x" * 43},
        )
        assert response.status_code == 404


def test_validation_rejects_invalid_people_count() -> None:
    invalid = payload()
    invalid["peopleCount"] = 0
    with TestClient(app) as client:
        assert client.post("/api/v1/relief-requests", json=invalid).status_code == 422
