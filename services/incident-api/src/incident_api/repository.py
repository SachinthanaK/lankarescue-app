import asyncio
from typing import Protocol

from .models import ReliefRequestRecord


class ReliefRequestRepository(Protocol):
    async def add(self, record: ReliefRequestRecord) -> None: ...

    async def get_by_reference(self, reference: str) -> ReliefRequestRecord | None: ...

    async def list_recent(self, limit: int = 100) -> list[ReliefRequestRecord]: ...


class InMemoryReliefRequestRepository:
    """Phase 1 adapter. Phase 2 replaces this without changing API handlers."""

    def __init__(self) -> None:
        self._records: dict[str, ReliefRequestRecord] = {}
        self._lock = asyncio.Lock()

    async def add(self, record: ReliefRequestRecord) -> None:
        async with self._lock:
            self._records[record.reference] = record

    async def get_by_reference(self, reference: str) -> ReliefRequestRecord | None:
        async with self._lock:
            return self._records.get(reference.upper())

    async def list_recent(self, limit: int = 100) -> list[ReliefRequestRecord]:
        async with self._lock:
            records = sorted(self._records.values(), key=lambda item: item.created_at, reverse=True)
            return records[:limit]

    async def clear(self) -> None:
        async with self._lock:
            self._records.clear()
