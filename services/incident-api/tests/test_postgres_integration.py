import os
import secrets
from datetime import UTC, datetime

import pytest
from incident_api.models import (
    ContactMethod,
    District,
    NeedType,
    Priority,
    ReliefRequestRecord,
    RequestStatus,
)
from incident_api.orm import AuditEventRow, ReliefRequestRow, RequestStatusHistoryRow
from incident_api.postgres_repository import SqlAlchemyReliefRequestRepository
from incident_api.repository import ConcurrentUpdateError
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_POSTGRES_TESTS") != "1",
    reason="Set RUN_POSTGRES_TESTS=1 after starting and migrating local PostgreSQL.",
)

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://lankarescue:local-development-only@localhost:5432/lankarescue",
)


def new_record() -> ReliefRequestRecord:
    suffix = secrets.token_hex(4).upper()
    return ReliefRequestRecord(
        reference=f"REQ-{datetime.now(UTC).year}-{suffix}",
        token_hash=secrets.token_hex(32),
        district=District.COLOMBO,
        location="Integration Test Center",
        need_type=NeedType.WATER,
        people_count=3,
        priority=Priority.URGENT,
        description="Synthetic integration-test request for database verification.",
        contact_method=ContactMethod.EMAIL,
        contact_value="integration@example.test",
    )


@pytest.mark.asyncio
@pytest.mark.integration
async def test_request_history_audit_and_concurrency_commit_atomically() -> None:
    engine = create_async_engine(DATABASE_URL)
    sessions = async_sessionmaker(engine, expire_on_commit=False)
    record = new_record()

    async with sessions() as session:
        await SqlAlchemyReliefRequestRepository(session).add(record)

    async with sessions() as session:
        stored_hash = await session.scalar(
            select(ReliefRequestRow.token_hash).where(ReliefRequestRow.id == record.id)
        )
        assert stored_hash == record.token_hash
        assert len(stored_hash or "") == 64

    async with sessions() as session:
        updated = await SqlAlchemyReliefRequestRepository(session).transition(
            reference=record.reference,
            target=RequestStatus.TRIAGED,
            actor="integration-coordinator@example.test",
            expected_version=1,
            reason=None,
            correlation_id="phase-2-integration",
        )
        assert updated.version == 2

    async with sessions() as session:
        history_count = await session.scalar(
            select(func.count())
            .select_from(RequestStatusHistoryRow)
            .where(RequestStatusHistoryRow.request_id == record.id)
        )
        audit_count = await session.scalar(
            select(func.count())
            .select_from(AuditEventRow)
            .where(AuditEventRow.entity_id == str(record.id))
        )
        assert history_count == 2
        assert audit_count == 2

    async with sessions() as session:
        with pytest.raises(ConcurrentUpdateError):
            await SqlAlchemyReliefRequestRepository(session).transition(
                reference=record.reference,
                target=RequestStatus.VERIFIED,
                actor="integration-coordinator@example.test",
                expected_version=1,
                reason=None,
                correlation_id="phase-2-stale-write",
            )

    async with sessions() as session:
        state = await session.scalar(
            select(ReliefRequestRow.status).where(ReliefRequestRow.id == record.id)
        )
        assert state == RequestStatus.TRIAGED.value

    await engine.dispose()
