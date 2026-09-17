from datetime import datetime
from typing import Annotated, Any
from uuid import UUID

from pydantic import BaseModel, Field, StringConstraints, model_validator

from .models import District, RequestStatus

Actor = Annotated[str, StringConstraints(strip_whitespace=True, min_length=2, max_length=120)]
Reason = Annotated[str, StringConstraints(strip_whitespace=True, min_length=3, max_length=500)]


class LifecycleUpdate(BaseModel):
    status: RequestStatus
    actor: Actor
    expected_version: int = Field(ge=1, alias="expectedVersion")
    reason: Reason | None = None
    correlation_id: str | None = Field(default=None, max_length=100, alias="correlationId")

    model_config = {"populate_by_name": True}


class StatusHistoryView(BaseModel):
    from_status: RequestStatus | None = Field(alias="fromStatus")
    to_status: RequestStatus = Field(alias="toStatus")
    actor: str
    reason: str | None
    request_version: int = Field(alias="requestVersion")
    changed_at: datetime = Field(alias="changedAt")

    model_config = {"populate_by_name": True}


class CenterCreate(BaseModel):
    name: Annotated[str, StringConstraints(strip_whitespace=True, min_length=2, max_length=160)]
    district: District
    location: Annotated[str, StringConstraints(strip_whitespace=True, min_length=2, max_length=240)]
    capacity: int = Field(ge=1, le=100_000)


class CenterView(CenterCreate):
    id: UUID
    current_occupancy: int = Field(alias="currentOccupancy")
    active: bool
    version: int

    model_config = {"populate_by_name": True}


class InventoryCreate(BaseModel):
    center_id: UUID = Field(alias="centerId")
    resource_type: Annotated[
        str, StringConstraints(strip_whitespace=True, min_length=2, max_length=80)
    ] = Field(alias="resourceType")
    quantity: int = Field(ge=0, le=10_000_000)
    unit: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=30)]

    model_config = {"populate_by_name": True}


class InventoryView(InventoryCreate):
    id: UUID
    reserved_quantity: int = Field(alias="reservedQuantity")
    version: int


class AssignmentCreate(BaseModel):
    request_reference: str = Field(min_length=8, max_length=40, alias="requestReference")
    center_id: UUID | None = Field(default=None, alias="centerId")
    volunteer_id: UUID | None = Field(default=None, alias="volunteerId")
    actor: Actor
    expected_version: int = Field(ge=1, alias="expectedVersion")
    notes: Annotated[str, StringConstraints(strip_whitespace=True, max_length=500)] | None = None

    model_config = {"populate_by_name": True}

    @model_validator(mode="after")
    def require_assignment_target(self) -> AssignmentCreate:
        if self.center_id is None and self.volunteer_id is None:
            raise ValueError("Either centerId or volunteerId is required.")
        return self


class AssignmentView(BaseModel):
    id: UUID
    request_reference: str = Field(alias="requestReference")
    center_id: UUID | None = Field(alias="centerId")
    volunteer_id: UUID | None = Field(alias="volunteerId")
    status: str
    assigned_by: str = Field(alias="assignedBy")
    created_at: datetime = Field(alias="createdAt")

    model_config = {"populate_by_name": True}


class AuditEventView(BaseModel):
    id: UUID
    actor: str
    action: str
    entity_type: str = Field(alias="entityType")
    entity_id: str = Field(alias="entityId")
    previous_state: dict[str, Any] | None = Field(alias="previousState")
    new_state: dict[str, Any] | None = Field(alias="newState")
    correlation_id: str | None = Field(alias="correlationId")
    created_at: datetime = Field(alias="createdAt")

    model_config = {"populate_by_name": True}
