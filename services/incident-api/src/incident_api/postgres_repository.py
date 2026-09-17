from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from .lifecycle import validate_transition
from .models import District, ReliefRequestRecord, RequestStatus
from .orm import (
    AssignmentRow,
    AuditEventRow,
    DistrictRow,
    IncidentRow,
    ReliefCenterRow,
    ReliefRequestRow,
    RequestStatusHistoryRow,
    ResourceInventoryRow,
)
from .repository import ConcurrentUpdateError, EntityNotFoundError
from .staff_models import (
    AssignmentCreate,
    AssignmentView,
    AuditEventView,
    CenterCreate,
    CenterView,
    InventoryCreate,
    InventoryView,
    StatusHistoryView,
)


class SqlAlchemyReliefRequestRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @staticmethod
    def _request_record(row: ReliefRequestRow, district_name: str) -> ReliefRequestRecord:
        return ReliefRequestRecord(
            id=row.id,
            reference=row.reference,
            token_hash=row.token_hash,
            incident_id=row.incident_id,
            district=District(district_name),
            location=row.location,
            need_type=row.need_type,
            people_count=row.people_count,
            priority=row.priority,
            description=row.description,
            contact_method=row.contact_method,
            contact_value=row.contact_value,
            status=row.status,
            version=row.version,
            created_at=row.created_at,
            updated_at=row.updated_at,
        )

    async def add(self, record: ReliefRequestRecord) -> None:
        async with self._session.begin():
            district = await self._session.scalar(
                select(DistrictRow).where(DistrictRow.name == record.district.value)
            )
            if district is None:
                raise EntityNotFoundError(f"District {record.district.value} is not seeded.")
            incident_id = await self._session.scalar(
                select(IncidentRow.id)
                .where(IncidentRow.status == "active")
                .order_by(IncidentRow.starts_at.desc())
                .limit(1)
            )
            row = ReliefRequestRow(
                id=record.id,
                reference=record.reference,
                token_hash=record.token_hash,
                incident_id=incident_id,
                district_code=district.code,
                location=record.location,
                need_type=record.need_type.value,
                people_count=record.people_count,
                priority=record.priority.value,
                description=record.description,
                contact_method=record.contact_method.value,
                contact_value=record.contact_value,
                status=record.status.value,
                version=record.version,
                created_at=record.created_at,
                updated_at=record.updated_at,
            )
            self._session.add(row)
            self._session.add(
                RequestStatusHistoryRow(
                    request_id=record.id,
                    from_status=None,
                    to_status=RequestStatus.SUBMITTED.value,
                    actor="anonymous-citizen",
                    reason="Request submitted",
                    request_version=1,
                )
            )
            self._session.add(
                AuditEventRow(
                    actor="anonymous-citizen",
                    action="relief_request.created",
                    entity_type="relief_request",
                    entity_id=str(record.id),
                    previous_state=None,
                    new_state={"status": RequestStatus.SUBMITTED.value, "version": 1},
                )
            )
            record.incident_id = incident_id

    async def get_by_reference(self, reference: str) -> ReliefRequestRecord | None:
        result = await self._session.execute(
            select(ReliefRequestRow, DistrictRow.name)
            .join(DistrictRow, DistrictRow.code == ReliefRequestRow.district_code)
            .where(ReliefRequestRow.reference == reference.upper())
        )
        item = result.one_or_none()
        if item is None:
            return None
        row, district_name = item
        return self._request_record(row, district_name)

    async def list_recent(self, limit: int = 100) -> list[ReliefRequestRecord]:
        result = await self._session.execute(
            select(ReliefRequestRow, DistrictRow.name)
            .join(DistrictRow, DistrictRow.code == ReliefRequestRow.district_code)
            .order_by(ReliefRequestRow.created_at.desc())
            .limit(limit)
        )
        return [self._request_record(row, district_name) for row, district_name in result.all()]

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
        async with self._session.begin():
            result = await self._session.execute(
                select(ReliefRequestRow, DistrictRow.name)
                .join(DistrictRow, DistrictRow.code == ReliefRequestRow.district_code)
                .where(ReliefRequestRow.reference == reference.upper())
            )
            item = result.one_or_none()
            if item is None:
                raise EntityNotFoundError("Relief request not found.")
            current_row, district_name = item
            current_status = RequestStatus(current_row.status)
            validate_transition(current_status, target, reason)
            now = datetime.now(UTC)
            updated = await self._session.scalar(
                update(ReliefRequestRow)
                .where(
                    ReliefRequestRow.id == current_row.id,
                    ReliefRequestRow.version == expected_version,
                )
                .values(status=target.value, version=expected_version + 1, updated_at=now)
                .returning(ReliefRequestRow)
            )
            if updated is None:
                raise ConcurrentUpdateError(
                    "The request changed after it was loaded. "
                    "Refresh and retry with the latest version."
                )
            self._session.add(
                RequestStatusHistoryRow(
                    request_id=updated.id,
                    from_status=current_status.value,
                    to_status=target.value,
                    actor=actor,
                    reason=reason,
                    request_version=updated.version,
                    changed_at=now,
                )
            )
            self._session.add(
                AuditEventRow(
                    actor=actor,
                    action="relief_request.status_changed",
                    entity_type="relief_request",
                    entity_id=str(updated.id),
                    previous_state={
                        "status": current_status.value,
                        "version": expected_version,
                    },
                    new_state={"status": target.value, "version": updated.version},
                    correlation_id=correlation_id,
                    created_at=now,
                )
            )
            return self._request_record(updated, district_name)

    async def list_history(self, reference: str) -> list[StatusHistoryView]:
        request_id = await self._session.scalar(
            select(ReliefRequestRow.id).where(ReliefRequestRow.reference == reference.upper())
        )
        if request_id is None:
            raise EntityNotFoundError("Relief request not found.")
        rows = (
            await self._session.scalars(
                select(RequestStatusHistoryRow)
                .where(RequestStatusHistoryRow.request_id == request_id)
                .order_by(RequestStatusHistoryRow.changed_at)
            )
        ).all()
        return [
            StatusHistoryView(
                from_status=row.from_status,
                to_status=row.to_status,
                actor=row.actor,
                reason=row.reason,
                request_version=row.request_version,
                changed_at=row.changed_at,
            )
            for row in rows
        ]

    async def create_center(self, request: CenterCreate, actor: str) -> CenterView:
        async with self._session.begin():
            district_code = await self._session.scalar(
                select(DistrictRow.code).where(DistrictRow.name == request.district.value)
            )
            if district_code is None:
                raise EntityNotFoundError("District is not seeded.")
            row = ReliefCenterRow(
                name=request.name,
                district_code=district_code,
                location=request.location,
                capacity=request.capacity,
            )
            self._session.add(row)
            await self._session.flush()
            self._session.add(
                AuditEventRow(
                    actor=actor,
                    action="relief_center.created",
                    entity_type="relief_center",
                    entity_id=str(row.id),
                    new_state={"district": request.district.value, "capacity": request.capacity},
                )
            )
            return self._center_view(row, request.district)

    async def list_centers(self) -> list[CenterView]:
        result = await self._session.execute(
            select(ReliefCenterRow, DistrictRow.name)
            .join(DistrictRow, DistrictRow.code == ReliefCenterRow.district_code)
            .order_by(ReliefCenterRow.name)
        )
        return [self._center_view(row, District(name)) for row, name in result.all()]

    @staticmethod
    def _center_view(row: ReliefCenterRow, district: District) -> CenterView:
        return CenterView(
            id=row.id,
            name=row.name,
            district=district,
            location=row.location,
            capacity=row.capacity,
            current_occupancy=row.current_occupancy,
            active=row.active,
            version=row.version,
        )

    async def create_inventory(self, request: InventoryCreate, actor: str) -> InventoryView:
        async with self._session.begin():
            center_exists = await self._session.scalar(
                select(ReliefCenterRow.id).where(ReliefCenterRow.id == request.center_id)
            )
            if center_exists is None:
                raise EntityNotFoundError("Relief center not found.")
            row = ResourceInventoryRow(
                center_id=request.center_id,
                resource_type=request.resource_type,
                quantity=request.quantity,
                unit=request.unit,
            )
            self._session.add(row)
            await self._session.flush()
            self._session.add(
                AuditEventRow(
                    actor=actor,
                    action="resource_inventory.created",
                    entity_type="resource_inventory",
                    entity_id=str(row.id),
                    new_state={"quantity": request.quantity, "unit": request.unit},
                )
            )
            return self._inventory_view(row)

    async def list_inventory(self, center_id: UUID | None = None) -> list[InventoryView]:
        statement = select(ResourceInventoryRow).order_by(ResourceInventoryRow.resource_type)
        if center_id is not None:
            statement = statement.where(ResourceInventoryRow.center_id == center_id)
        rows = (await self._session.scalars(statement)).all()
        return [self._inventory_view(row) for row in rows]

    @staticmethod
    def _inventory_view(row: ResourceInventoryRow) -> InventoryView:
        return InventoryView(
            id=row.id,
            center_id=row.center_id,
            resource_type=row.resource_type,
            quantity=row.quantity,
            reserved_quantity=row.reserved_quantity,
            unit=row.unit,
            version=row.version,
        )

    async def create_assignment(self, request: AssignmentCreate) -> AssignmentView:
        async with self._session.begin():
            row = await self._session.scalar(
                select(ReliefRequestRow).where(
                    ReliefRequestRow.reference == request.request_reference.upper()
                )
            )
            if row is None:
                raise EntityNotFoundError("Relief request not found.")
            current_status = RequestStatus(row.status)
            validate_transition(current_status, RequestStatus.ASSIGNED, request.notes)
            updated = await self._session.scalar(
                update(ReliefRequestRow)
                .where(
                    ReliefRequestRow.id == row.id,
                    ReliefRequestRow.version == request.expected_version,
                )
                .values(
                    status=RequestStatus.ASSIGNED.value,
                    version=request.expected_version + 1,
                    updated_at=datetime.now(UTC),
                )
                .returning(ReliefRequestRow)
            )
            if updated is None:
                raise ConcurrentUpdateError("The request version is stale.")
            assignment = AssignmentRow(
                request_id=row.id,
                center_id=request.center_id,
                volunteer_id=request.volunteer_id,
                notes=request.notes,
                assigned_by=request.actor,
            )
            self._session.add(assignment)
            await self._session.flush()
            self._session.add_all(
                [
                    RequestStatusHistoryRow(
                        request_id=row.id,
                        from_status=current_status.value,
                        to_status=RequestStatus.ASSIGNED.value,
                        actor=request.actor,
                        reason=request.notes,
                        request_version=updated.version,
                    ),
                    AuditEventRow(
                        actor=request.actor,
                        action="relief_request.assigned",
                        entity_type="relief_request",
                        entity_id=str(row.id),
                        previous_state={"status": current_status.value},
                        new_state={
                            "status": RequestStatus.ASSIGNED.value,
                            "assignmentId": str(assignment.id),
                        },
                    ),
                ]
            )
            return AssignmentView(
                id=assignment.id,
                request_reference=row.reference,
                center_id=assignment.center_id,
                volunteer_id=assignment.volunteer_id,
                status=assignment.status,
                assigned_by=assignment.assigned_by,
                created_at=assignment.created_at,
            )

    async def list_audit_events(self, limit: int = 100) -> list[AuditEventView]:
        rows = (
            await self._session.scalars(
                select(AuditEventRow).order_by(AuditEventRow.created_at.desc()).limit(limit)
            )
        ).all()
        return [
            AuditEventView(
                id=row.id,
                actor=row.actor,
                action=row.action,
                entity_type=row.entity_type,
                entity_id=row.entity_id,
                previous_state=row.previous_state,
                new_state=row.new_state,
                correlation_id=row.correlation_id,
                created_at=row.created_at,
            )
            for row in rows
        ]
