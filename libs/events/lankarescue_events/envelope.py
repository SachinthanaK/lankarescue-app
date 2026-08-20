from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class EventEnvelope(BaseModel):
    """Stable metadata shared by all LankaRescue integration events."""

    event_id: UUID = Field(default_factory=uuid4, alias="eventId")
    event_type: str = Field(alias="eventType")
    schema_version: int = Field(default=1, alias="schemaVersion")
    occurred_at: datetime = Field(default_factory=lambda: datetime.now(UTC), alias="occurredAt")
    correlation_id: str = Field(alias="correlationId")
    payload: dict[str, Any]

    model_config = {"populate_by_name": True}
