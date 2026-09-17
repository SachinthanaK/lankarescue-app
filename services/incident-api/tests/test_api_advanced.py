import pytest
from fastapi.testclient import TestClient
from incident_api.dependencies import get_repository
from incident_api.main import app
from incident_api.repository import InMemoryReliefRequestRepository


from collections.abc import Iterator

@pytest.fixture
def client() -> Iterator[TestClient]:
    repository = InMemoryReliefRequestRepository()
    app.dependency_overrides[get_repository] = lambda: repository
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

def payload() -> dict[str, object]:
    return {
        "district": "Colombo",
        "location": "Colombo Fort",
        "needType": "water",
        "peopleCount": 5,
        "priority": "urgent",
        "description": "Need water",
        "contactMethod": "phone",
        "contactValue": "0771234567",
    }

def test_validation_rejects_missing_fields(client: TestClient) -> None:
    data = payload()
    del data["district"]
    response = client.post("/api/v1/relief-requests", json=data)
    assert response.status_code == 422
    assert "district" in response.text

def test_validation_rejects_invalid_priority(client: TestClient) -> None:
    data = payload()
    data["priority"] = "super-urgent"
    response = client.post("/api/v1/relief-requests", json=data)
    assert response.status_code == 422

def test_track_with_wrong_reference_fails(client: TestClient) -> None:
    created = client.post("/api/v1/relief-requests", json=payload()).json()
    response = client.post(
        "/api/v1/relief-requests/track",
        json={"reference": "REQ-INVALID", "trackingToken": created["trackingToken"]},
    )
    assert response.status_code == 404

def test_staff_status_transition_success(client: TestClient) -> None:
    created = client.post("/api/v1/relief-requests", json=payload()).json()
    ref = created["reference"]
    
    # Transition to TRIAGED (valid from SUBMITTED)
    update_payload = {
        "status": "triaged",
        "actor": "demo-staff",
        "expectedVersion": 1,
        "reason": None
    }
    response = client.put(
        f"/api/v1/demo/staff/relief-requests/{ref}/status",
        json=update_payload,
        headers={"X-Demo-Actor": "demo-staff"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "triaged"
    assert response.json()["version"] == 2

def test_staff_status_transition_invalid_target_fails(client: TestClient) -> None:
    created = client.post("/api/v1/relief-requests", json=payload()).json()
    ref = created["reference"]
    
    # Transition to IN_PROGRESS directly from SUBMITTED is invalid
    update_payload = {
        "status": "in_progress",
        "actor": "demo-staff",
        "expectedVersion": 1,
        "reason": None
    }
    response = client.put(
        f"/api/v1/demo/staff/relief-requests/{ref}/status",
        json=update_payload,
        headers={"X-Demo-Actor": "demo-staff"}
    )
    assert "Cannot transition" in response.text or "not allowed" in response.text

def test_staff_status_transition_optimistic_concurrency_fails(client: TestClient) -> None:
    created = client.post("/api/v1/relief-requests", json=payload()).json()
    ref = created["reference"]
    
    # Transition to TRIAGED
    update_payload = {"status": "triaged", "actor": "demo-staff", "expectedVersion": 1}
    client.put(f"/api/v1/demo/staff/relief-requests/{ref}/status", json=update_payload)
    
    # Try transitioning again with stale version (1) instead of 2
    update_payload2 = {"status": "verified", "actor": "demo-staff", "expectedVersion": 1}
    response2 = client.put(f"/api/v1/demo/staff/relief-requests/{ref}/status", json=update_payload2)
    assert response2.status_code == 409
