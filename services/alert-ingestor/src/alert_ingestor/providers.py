from datetime import UTC, datetime
from typing import Protocol

from pydantic import BaseModel


class ProviderAlert(BaseModel):
    provider_id: str
    headline: str
    severity: str
    observed_at: datetime


class AlertProvider(Protocol):
    async def fetch(self) -> list[ProviderAlert]: ...


class MockAlertProvider:
    """Deterministic local provider; real providers arrive in Phase 4."""

    async def fetch(self) -> list[ProviderAlert]:
        return [
            ProviderAlert(
                provider_id="mock-weather-001",
                headline="Demo flood warning for local development",
                severity="moderate",
                observed_at=datetime.now(UTC),
            )
        ]
