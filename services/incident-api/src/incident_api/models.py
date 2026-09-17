from datetime import UTC, datetime
from enum import StrEnum
from typing import Annotated
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, StringConstraints, field_validator

ShortText = Annotated[str, StringConstraints(strip_whitespace=True, min_length=2, max_length=120)]
Description = Annotated[
    str, StringConstraints(strip_whitespace=True, min_length=10, max_length=2000)
]
TrackingToken = Annotated[str, StringConstraints(min_length=32, max_length=128)]


class District(StrEnum):
    AMPARA = "Ampara"
    ANURADHAPURA = "Anuradhapura"
    BADULLA = "Badulla"
    BATTICALOA = "Batticaloa"
    COLOMBO = "Colombo"
    GALLE = "Galle"
    GAMPAHA = "Gampaha"
    HAMBANTOTA = "Hambantota"
    JAFFNA = "Jaffna"
    KALUTARA = "Kalutara"
    KANDY = "Kandy"
    KEGALLE = "Kegalle"
    KILINOCHCHI = "Kilinochchi"
    KURUNEGALA = "Kurunegala"
    MANNAR = "Mannar"
    MATALE = "Matale"
    MATARA = "Matara"
    MONARAGALA = "Monaragala"
    MULLAITIVU = "Mullaitivu"
    NUWARA_ELIYA = "Nuwara Eliya"
    POLONNARUWA = "Polonnaruwa"
    PUTTALAM = "Puttalam"
    RATNAPURA = "Ratnapura"
    TRINCOMALEE = "Trincomalee"
    VAVUNIYA = "Vavuniya"


class NeedType(StrEnum):
    FOOD = "food"
    WATER = "water"
    MEDICAL = "medical"
    SHELTER = "shelter"
    EVACUATION = "evacuation"
    OTHER = "other"


class Priority(StrEnum):
    NORMAL = "normal"
    URGENT = "urgent"
    CRITICAL = "critical"


class ContactMethod(StrEnum):
    PHONE = "phone"
    SMS = "sms"
    EMAIL = "email"


class RequestStatus(StrEnum):
    SUBMITTED = "submitted"
    TRIAGED = "triaged"
    VERIFIED = "verified"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    REJECTED = "rejected"
    CANCELLED = "cancelled"


class ReliefRequestCreate(BaseModel):
    district: District
    location: ShortText
    need_type: NeedType = Field(alias="needType")
    people_count: int = Field(ge=1, le=500, alias="peopleCount")
    priority: Priority = Priority.NORMAL
    description: Description
    contact_method: ContactMethod = Field(alias="contactMethod")
    contact_value: ShortText = Field(alias="contactValue")

    model_config = {"populate_by_name": True}

    @field_validator("contact_value")
    @classmethod
    def reject_control_characters(cls, value: str) -> str:
        if any(ord(character) < 32 for character in value):
            raise ValueError("contactValue contains invalid characters")
        return value


class ReliefRequestRecord(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    reference: str
    token_hash: str
    incident_id: UUID | None = None
    district: District
    location: str
    need_type: NeedType
    people_count: int
    priority: Priority
    description: str
    contact_method: ContactMethod
    contact_value: str
    status: RequestStatus = RequestStatus.SUBMITTED
    version: int = 1
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class ReliefRequestCreated(BaseModel):
    reference: str
    tracking_token: str = Field(alias="trackingToken")
    status: RequestStatus
    created_at: datetime = Field(alias="createdAt")
    message: str

    model_config = {"populate_by_name": True}


class TrackRequest(BaseModel):
    reference: Annotated[str, StringConstraints(strip_whitespace=True, min_length=8, max_length=40)]
    tracking_token: TrackingToken = Field(alias="trackingToken")

    model_config = {"populate_by_name": True}


class ReliefRequestView(BaseModel):
    reference: str
    district: District
    location: str
    need_type: NeedType = Field(alias="needType")
    people_count: int = Field(alias="peopleCount")
    priority: Priority
    description: str
    status: RequestStatus
    version: int
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")

    model_config = {"populate_by_name": True}

    @classmethod
    def from_record(cls, record: ReliefRequestRecord) -> ReliefRequestView:
        return cls.model_validate(
            record.model_dump(exclude={"id", "token_hash", "contact_method", "contact_value"})
        )


class DemoQueueItem(ReliefRequestView):
    contact_method: ContactMethod = Field(alias="contactMethod")
    contact_value: str = Field(alias="contactValue")

    @classmethod
    def from_record(cls, record: ReliefRequestRecord) -> DemoQueueItem:
        return cls.model_validate(record.model_dump(exclude={"id", "token_hash"}))
