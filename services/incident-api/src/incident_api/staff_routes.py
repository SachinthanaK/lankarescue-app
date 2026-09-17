from typing import Annotated, NoReturn
from uuid import UUID

from fastapi import APIRouter, Depends, Header, HTTPException, Query, Request, status

from .dependencies import get_repository, require_demo_staff
from .lifecycle import InvalidTransitionError, ReasonRequiredError
from .models import ReliefRequestView
from .postgres_repository import SqlAlchemyReliefRequestRepository
from .repository import ConcurrentUpdateError, EntityNotFoundError
from .staff_models import (
    AssignmentCreate,
    AssignmentView,
    AuditEventView,
    CenterCreate,
    CenterView,
    InventoryCreate,
    InventoryView,
    LifecycleUpdate,
    StatusHistoryView,
)

router = APIRouter(
    prefix="/api/v1/demo/staff",
    tags=["local demo operations"],
    dependencies=[Depends(require_demo_staff)],
)


def raise_domain_http(error: Exception) -> NoReturn:
    if isinstance(error, EntityNotFoundError):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error
    if isinstance(error, ConcurrentUpdateError):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error)) from error
    if isinstance(error, (InvalidTransitionError, ReasonRequiredError)):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=str(error),
        ) from error
    raise error


@router.put(
    "/relief-requests/{reference}/status",
    response_model=ReliefRequestView,
)
async def update_status(
    reference: str,
    update: LifecycleUpdate,
    request: Request,
    repository: Annotated[SqlAlchemyReliefRequestRepository, Depends(get_repository)],
) -> ReliefRequestView:
    try:
        record = await repository.transition(
            reference=reference,
            target=update.status,
            actor=update.actor,
            expected_version=update.expected_version,
            reason=update.reason,
            correlation_id=update.correlation_id or request.state.correlation_id,
        )
        return ReliefRequestView.from_record(record)
    except (
        EntityNotFoundError,
        ConcurrentUpdateError,
        InvalidTransitionError,
        ReasonRequiredError,
    ) as error:
        raise_domain_http(error)


@router.get(
    "/relief-requests/{reference}/history",
    response_model=list[StatusHistoryView],
)
async def request_history(
    reference: str,
    repository: Annotated[SqlAlchemyReliefRequestRepository, Depends(get_repository)],
) -> list[StatusHistoryView]:
    try:
        return await repository.list_history(reference)
    except EntityNotFoundError as error:
        raise_domain_http(error)


@router.post("/centers", response_model=CenterView, status_code=status.HTTP_201_CREATED)
async def create_center(
    center: CenterCreate,
    repository: Annotated[SqlAlchemyReliefRequestRepository, Depends(get_repository)],
    actor: Annotated[
        str, Header(alias="X-Demo-Actor", min_length=2, max_length=120)
    ] = "demo-coordinator",
) -> CenterView:
    try:
        return await repository.create_center(center, actor)
    except EntityNotFoundError as error:
        raise_domain_http(error)


@router.get("/centers", response_model=list[CenterView])
async def list_centers(
    repository: Annotated[SqlAlchemyReliefRequestRepository, Depends(get_repository)],
) -> list[CenterView]:
    return await repository.list_centers()


@router.post("/inventory", response_model=InventoryView, status_code=status.HTTP_201_CREATED)
async def create_inventory(
    inventory: InventoryCreate,
    repository: Annotated[SqlAlchemyReliefRequestRepository, Depends(get_repository)],
    actor: Annotated[
        str, Header(alias="X-Demo-Actor", min_length=2, max_length=120)
    ] = "demo-coordinator",
) -> InventoryView:
    try:
        return await repository.create_inventory(inventory, actor)
    except EntityNotFoundError as error:
        raise_domain_http(error)


@router.get("/inventory", response_model=list[InventoryView])
async def list_inventory(
    repository: Annotated[SqlAlchemyReliefRequestRepository, Depends(get_repository)],
    center_id: Annotated[UUID | None, Query(alias="centerId")] = None,
) -> list[InventoryView]:
    return await repository.list_inventory(center_id)


@router.post("/assignments", response_model=AssignmentView, status_code=status.HTTP_201_CREATED)
async def create_assignment(
    assignment: AssignmentCreate,
    repository: Annotated[SqlAlchemyReliefRequestRepository, Depends(get_repository)],
) -> AssignmentView:
    try:
        return await repository.create_assignment(assignment)
    except (EntityNotFoundError, ConcurrentUpdateError, InvalidTransitionError) as error:
        raise_domain_http(error)


@router.get("/audit-events", response_model=list[AuditEventView])
async def list_audit_events(
    repository: Annotated[SqlAlchemyReliefRequestRepository, Depends(get_repository)],
    limit: Annotated[int, Query(ge=1, le=500)] = 100,
) -> list[AuditEventView]:
    return await repository.list_audit_events(limit)
