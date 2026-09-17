from .models import RequestStatus


class InvalidTransitionError(ValueError):
    pass


class ReasonRequiredError(ValueError):
    pass


ALLOWED_TRANSITIONS: dict[RequestStatus, frozenset[RequestStatus]] = {
    RequestStatus.SUBMITTED: frozenset({RequestStatus.TRIAGED, RequestStatus.CANCELLED}),
    RequestStatus.TRIAGED: frozenset(
        {RequestStatus.VERIFIED, RequestStatus.REJECTED, RequestStatus.CANCELLED}
    ),
    RequestStatus.VERIFIED: frozenset(
        {RequestStatus.ASSIGNED, RequestStatus.REJECTED, RequestStatus.CANCELLED}
    ),
    RequestStatus.ASSIGNED: frozenset({RequestStatus.IN_PROGRESS, RequestStatus.CANCELLED}),
    RequestStatus.IN_PROGRESS: frozenset({RequestStatus.COMPLETED, RequestStatus.CANCELLED}),
    RequestStatus.COMPLETED: frozenset(),
    RequestStatus.REJECTED: frozenset(),
    RequestStatus.CANCELLED: frozenset(),
}

REASON_REQUIRED = frozenset({RequestStatus.REJECTED, RequestStatus.CANCELLED})


def validate_transition(
    current: RequestStatus,
    target: RequestStatus,
    reason: str | None,
) -> None:
    if target not in ALLOWED_TRANSITIONS[current]:
        raise InvalidTransitionError(f"Cannot transition from {current.value} to {target.value}.")
    if target in REASON_REQUIRED and not reason:
        raise ReasonRequiredError(f"A reason is required when moving to {target.value}.")
