from datetime import UTC, datetime
from typing import Any
from uuid import UUID

from lankarescue_database import Base, TimestampMixin, UuidPrimaryKeyMixin
from sqlalchemy import (
    JSON,
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship


class DistrictRow(Base):
    __tablename__ = "districts"

    code: Mapped[str] = mapped_column(String(5), primary_key=True)
    name: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    province: Mapped[str] = mapped_column(String(80), nullable=False)


class IncidentRow(UuidPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "incidents"

    name: Mapped[str] = mapped_column(String(160), nullable=False)
    incident_type: Mapped[str] = mapped_column(String(60), nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="active")
    starts_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    ends_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    __table_args__ = (
        CheckConstraint("status IN ('planned','active','closed')", name="ck_incident_status"),
        Index("ix_incidents_status_starts_at", "status", "starts_at"),
    )


class ReliefRequestRow(UuidPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "relief_requests"

    reference: Mapped[str] = mapped_column(String(40), unique=True, nullable=False)
    token_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    incident_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("incidents.id", ondelete="SET NULL")
    )
    district_code: Mapped[str] = mapped_column(
        ForeignKey("districts.code", ondelete="RESTRICT"), nullable=False
    )
    location: Mapped[str] = mapped_column(String(120), nullable=False)
    need_type: Mapped[str] = mapped_column(String(30), nullable=False)
    people_count: Mapped[int] = mapped_column(Integer, nullable=False)
    priority: Mapped[str] = mapped_column(String(20), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    contact_method: Mapped[str] = mapped_column(String(20), nullable=False)
    contact_value: Mapped[str] = mapped_column(String(120), nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="submitted")
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    history: Mapped[list[RequestStatusHistoryRow]] = relationship(
        back_populates="request", cascade="all, delete-orphan"
    )

    __table_args__ = (
        CheckConstraint("people_count BETWEEN 1 AND 500", name="ck_request_people_count"),
        CheckConstraint("version >= 1", name="ck_request_version"),
        CheckConstraint("priority IN ('normal','urgent','critical')", name="ck_request_priority"),
        CheckConstraint(
            "status IN ('submitted','triaged','verified','assigned','in_progress',"
            "'completed','rejected','cancelled')",
            name="ck_request_status",
        ),
        Index("ix_requests_status_priority_created", "status", "priority", "created_at"),
        Index("ix_requests_district_status", "district_code", "status"),
    )


class RequestStatusHistoryRow(UuidPrimaryKeyMixin, Base):
    __tablename__ = "request_status_history"

    request_id: Mapped[UUID] = mapped_column(
        ForeignKey("relief_requests.id", ondelete="CASCADE"), nullable=False
    )
    from_status: Mapped[str | None] = mapped_column(String(30))
    to_status: Mapped[str] = mapped_column(String(30), nullable=False)
    actor: Mapped[str] = mapped_column(String(120), nullable=False)
    reason: Mapped[str | None] = mapped_column(String(500))
    request_version: Mapped[int] = mapped_column(Integer, nullable=False)
    changed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )

    request: Mapped[ReliefRequestRow] = relationship(back_populates="history")

    __table_args__ = (Index("ix_status_history_request_changed", "request_id", "changed_at"),)


class ReliefCenterRow(UuidPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "relief_centers"

    name: Mapped[str] = mapped_column(String(160), nullable=False)
    district_code: Mapped[str] = mapped_column(
        ForeignKey("districts.code", ondelete="RESTRICT"), nullable=False
    )
    location: Mapped[str] = mapped_column(String(240), nullable=False)
    capacity: Mapped[int] = mapped_column(Integer, nullable=False)
    current_occupancy: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    __table_args__ = (
        CheckConstraint("capacity > 0", name="ck_center_capacity"),
        CheckConstraint("current_occupancy BETWEEN 0 AND capacity", name="ck_center_occupancy"),
        UniqueConstraint("name", "district_code", name="uq_center_name_district"),
        Index("ix_centers_district_active", "district_code", "active"),
    )


class ResourceInventoryRow(UuidPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "resource_inventory"

    center_id: Mapped[UUID] = mapped_column(
        ForeignKey("relief_centers.id", ondelete="CASCADE"), nullable=False
    )
    resource_type: Mapped[str] = mapped_column(String(80), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    reserved_quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    unit: Mapped[str] = mapped_column(String(30), nullable=False)
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    __table_args__ = (
        CheckConstraint("quantity >= 0", name="ck_inventory_quantity"),
        CheckConstraint("reserved_quantity BETWEEN 0 AND quantity", name="ck_inventory_reserved"),
        UniqueConstraint("center_id", "resource_type", "unit", name="uq_inventory_item"),
        Index("ix_inventory_center_resource", "center_id", "resource_type"),
    )


class VolunteerRow(UuidPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "volunteers"

    display_name: Mapped[str] = mapped_column(String(120), nullable=False)
    contact_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    district_code: Mapped[str] = mapped_column(
        ForeignKey("districts.code", ondelete="RESTRICT"), nullable=False
    )
    skills: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    available: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    __table_args__ = (Index("ix_volunteers_district_available", "district_code", "available"),)


class AssignmentRow(UuidPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "assignments"

    request_id: Mapped[UUID] = mapped_column(
        ForeignKey("relief_requests.id", ondelete="CASCADE"), nullable=False
    )
    center_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("relief_centers.id", ondelete="SET NULL")
    )
    volunteer_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("volunteers.id", ondelete="SET NULL")
    )
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="active")
    notes: Mapped[str | None] = mapped_column(String(500))
    assigned_by: Mapped[str] = mapped_column(String(120), nullable=False)

    __table_args__ = (
        CheckConstraint(
            "center_id IS NOT NULL OR volunteer_id IS NOT NULL", name="ck_assignment_target"
        ),
        CheckConstraint(
            "status IN ('active','completed','cancelled')", name="ck_assignment_status"
        ),
        Index("ix_assignments_request_status", "request_id", "status"),
    )


class ApplicationRoleRow(UuidPrimaryKeyMixin, Base):
    __tablename__ = "application_roles"

    name: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(300), nullable=False)


class RoleBindingRow(UuidPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "role_bindings"

    subject_id: Mapped[str] = mapped_column(String(200), nullable=False)
    role_id: Mapped[UUID] = mapped_column(
        ForeignKey("application_roles.id", ondelete="CASCADE"), nullable=False
    )
    scope_type: Mapped[str] = mapped_column(String(40), nullable=False, default="global")
    scope_id: Mapped[str | None] = mapped_column(String(200))

    __table_args__ = (
        UniqueConstraint("subject_id", "role_id", "scope_type", "scope_id", name="uq_role_binding"),
        Index("ix_role_bindings_subject", "subject_id"),
    )


class AuditEventRow(UuidPrimaryKeyMixin, Base):
    __tablename__ = "audit_events"

    actor: Mapped[str] = mapped_column(String(120), nullable=False)
    action: Mapped[str] = mapped_column(String(100), nullable=False)
    entity_type: Mapped[str] = mapped_column(String(80), nullable=False)
    entity_id: Mapped[str] = mapped_column(String(80), nullable=False)
    previous_state: Mapped[dict[str, Any] | None] = mapped_column(JSON)
    new_state: Mapped[dict[str, Any] | None] = mapped_column(JSON)
    correlation_id: Mapped[str | None] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )

    __table_args__ = (
        Index("ix_audit_entity_created", "entity_type", "entity_id", "created_at"),
        Index("ix_audit_actor_created", "actor", "created_at"),
    )
