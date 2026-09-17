from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from .config import Settings, get_settings
from .database import get_session
from .postgres_repository import SqlAlchemyReliefRequestRepository


def get_repository(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> SqlAlchemyReliefRequestRepository:
    return SqlAlchemyReliefRequestRepository(session)


def require_demo_staff(settings: Annotated[Settings, Depends(get_settings)]) -> None:
    if settings.app_env != "local" or not settings.enable_demo_staff:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
