import secrets
from datetime import UTC, datetime

from lankarescue_auth import generate_tracking_token, hash_tracking_token, verify_tracking_token

from .models import ReliefRequestCreate, ReliefRequestRecord, RequestStatus
from .repository import EntityNotFoundError, ReliefRequestRepository


class RequestNotFoundError(Exception):
    pass


class ReliefRequestService:
    def __init__(self, repository: ReliefRequestRepository) -> None:
        self._repository = repository

    async def create(self, request: ReliefRequestCreate) -> tuple[ReliefRequestRecord, str]:
        token = generate_tracking_token()
        record = ReliefRequestRecord(
            reference=f"REQ-{datetime.now(UTC).year}-{secrets.token_hex(4).upper()}",
            token_hash=hash_tracking_token(token),
            **request.model_dump(),
        )
        await self._repository.add(record)
        return record, token

    async def track(self, reference: str, token: str) -> ReliefRequestRecord:
        record = await self._repository.get_by_reference(reference)
        if record is None or not verify_tracking_token(token, record.token_hash):
            raise RequestNotFoundError
        return record

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
        try:
            return await self._repository.transition(
                reference=reference,
                target=target,
                actor=actor,
                expected_version=expected_version,
                reason=reason,
                correlation_id=correlation_id,
            )
        except EntityNotFoundError as error:
            raise RequestNotFoundError from error
