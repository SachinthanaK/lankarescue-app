import asyncio
from datetime import UTC, datetime
from typing import Protocol

from .lifecycle import validate_transition
from .models import ReliefRequestRecord, RequestStatus


class ConcurrentUpdateError(RuntimeError):
    pass


class EntityNotFoundError(LookupError):
    pass


class ReliefRequestRepository(Protocol):
    async def add(self, record: ReliefRequestRecord) -> None: ...

    async def get_by_reference(self, reference: str) -> ReliefRequestRecord | None: ...

    async def list_recent(self, limit: int = 100) -> list[ReliefRequestRecord]: ...

    async def transition(
        self,
        *,
        reference: str,
        target: RequestStatus,
        actor: str,
        expected_version: int,
        reason: str | None,
        correlation_id: str | None,
    ) -> ReliefRequestRecord: ...


class InMemoryReliefRequestRepository:
    """Test adapter. Runtime persistence uses PostgreSQL from Phase 2 onward."""

    def __init__(self) -> None:
        self._records: dict[str, ReliefRequestRecord] = {}
        self._lock = asyncio.Lock()

    async def add(self, record: ReliefRequestRecord) -> None:
        async with self._lock:
            self._records[record.reference] = record

    async def get_by_reference(self, reference: str) -> ReliefRequestRecord | None:
        async with self._lock:
            record = self._records.get(reference.upper())
            return record.model_copy(deep=True) if record else None

    async def list_recent(self, limit: int = 100) -> list[ReliefRequestRecord]:
        async with self._lock:
            records = sorted(self._records.values(), key=lambda item: item.created_at, reverse=True)
            return [record.model_copy(deep=True) for record in records[:limit]]

    async def transition(
        self,
        *,
        reference: str,
        target: RequestStatus,
        actor: str,
        expected_version: int,
        reason: str | None,
        correlation_id: str | None,
    ) -> ReliefRequestRecord:
        del actor, correlation_id
        async with self._lock:
            record = self._records.get(reference.upper())
            if record is None:
                raise EntityNotFoundError("Relief request not found.")
            validate_transition(record.status, target, reason)
            if record.version != expected_version:
                raise ConcurrentUpdateError("The request version is stale.")
            record.status = target
            record.version += 1
            record.updated_at = datetime.now(UTC)
            return record.model_copy(deep=True)

    async def clear(self) -> None:
        async with self._lock:
            self._records.clear()
