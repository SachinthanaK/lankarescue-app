from typing import Annotated

from fastapi import Depends, HTTPException, Query, status
from lankarescue_observability import create_service_app

from .config import get_settings
from .database import database_ready
from .dependencies import get_repository, require_demo_staff
from .models import (
    DemoQueueItem,
    ReliefRequestCreate,
    ReliefRequestCreated,
    ReliefRequestView,
    TrackRequest,
)
from .postgres_repository import SqlAlchemyReliefRequestRepository
from .service import ReliefRequestService, RequestNotFoundError
from .staff_routes import router as staff_router

VERSION = "0.2.0"
settings = get_settings()

app = create_service_app(
    service_name="incident-api",
    version=VERSION,
    environment=settings.app_env,
    log_level=settings.log_level,
    allowed_origins=settings.allowed_origin_list,
    description="Persist, coordinate, and securely track LankaRescue relief requests.",
    readiness_check=database_ready,
)
app.include_router(staff_router)


def get_service(
    request_repository: Annotated[SqlAlchemyReliefRequestRepository, Depends(get_repository)],
) -> ReliefRequestService:
    return ReliefRequestService(request_repository)


@app.post(
    "/api/v1/relief-requests",
    response_model=ReliefRequestCreated,
    status_code=status.HTTP_201_CREATED,
    tags=["relief requests"],
)
async def create_relief_request(
    request: ReliefRequestCreate,
    service: Annotated[ReliefRequestService, Depends(get_service)],
) -> ReliefRequestCreated:
    record, token = await service.create(request)
    return ReliefRequestCreated(
        reference=record.reference,
        tracking_token=token,
        status=record.status,
        created_at=record.created_at,
        message="Save the reference and private tracking token. The token cannot be recovered.",
    )


@app.post(
    "/api/v1/relief-requests/track",
    response_model=ReliefRequestView,
    tags=["relief requests"],
)
async def track_relief_request(
    request: TrackRequest,
    service: Annotated[ReliefRequestService, Depends(get_service)],
) -> ReliefRequestView:
    try:
        record = await service.track(request.reference.upper(), request.tracking_token)
    except RequestNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Request not found. Check both the reference and private tracking token.",
        ) from error
    return ReliefRequestView.from_record(record)


@app.get(
    "/api/v1/demo/staff/relief-requests",
    response_model=list[DemoQueueItem],
    tags=["local demo"],
    dependencies=[Depends(require_demo_staff)],
)
async def demo_staff_queue(
    request_repository: Annotated[SqlAlchemyReliefRequestRepository, Depends(get_repository)],
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
) -> list[DemoQueueItem]:
    records = await request_repository.list_recent(limit)
    return [DemoQueueItem.from_record(record) for record in records]
