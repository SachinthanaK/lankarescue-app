from uuid import uuid4

import pytest
from incident_api.models import (
    ContactMethod,
    District,
    NeedType,
    Priority,
    ReliefRequestRecord,
    RequestStatus,
)
from incident_api.repository import ConcurrentUpdateError, InMemoryReliefRequestRepository


def record() -> ReliefRequestRecord:
    return ReliefRequestRecord(
        id=uuid4(),
        reference="REQ-2026-CONCUR01",
        token_hash="0" * 64,
        district=District.COLOMBO,
        location="Colombo Fort",
        need_type=NeedType.WATER,
        people_count=4,
        priority=Priority.URGENT,
        description="Drinking water required for four people.",
        contact_method=ContactMethod.PHONE,
        contact_value="+94 77 000 0000",
    )


@pytest.mark.asyncio
async def test_stale_version_cannot_overwrite_newer_state() -> None:
    repository = InMemoryReliefRequestRepository()
    await repository.add(record())
    first = await repository.transition(
        reference="REQ-2026-CONCUR01",
        target=RequestStatus.TRIAGED,
        actor="coordinator@example.test",
        expected_version=1,
        reason=None,
        correlation_id="test-1",
    )
    assert first.version == 2
    with pytest.raises(ConcurrentUpdateError):
        await repository.transition(
            reference="REQ-2026-CONCUR01",
            target=RequestStatus.VERIFIED,
            actor="coordinator@example.test",
            expected_version=1,
            reason=None,
            correlation_id="test-2",
        )
