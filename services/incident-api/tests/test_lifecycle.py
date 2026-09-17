import pytest
from incident_api.lifecycle import (
    ALLOWED_TRANSITIONS,
    InvalidTransitionError,
    ReasonRequiredError,
    validate_transition,
)
from incident_api.models import RequestStatus


@pytest.mark.parametrize(
    ("current", "target"),
    [
        (current, target)
        for current, targets in ALLOWED_TRANSITIONS.items()
        for target in targets
        if target not in {RequestStatus.CANCELLED, RequestStatus.REJECTED}
    ],
)
def test_every_allowed_transition_is_accepted(
    current: RequestStatus, target: RequestStatus
) -> None:
    validate_transition(current, target, None)


@pytest.mark.parametrize(
    ("current", "target"),
    [
        (current, target)
        for current in RequestStatus
        for target in RequestStatus
        if target not in ALLOWED_TRANSITIONS[current]
    ],
)
def test_every_disallowed_transition_is_rejected(
    current: RequestStatus, target: RequestStatus
) -> None:
    with pytest.raises(InvalidTransitionError):
        validate_transition(current, target, "documented reason")


@pytest.mark.parametrize("target", [RequestStatus.CANCELLED, RequestStatus.REJECTED])
def test_terminal_negative_transitions_require_reason(target: RequestStatus) -> None:
    current = (
        RequestStatus.SUBMITTED if target is RequestStatus.CANCELLED else RequestStatus.TRIAGED
    )
    with pytest.raises(ReasonRequiredError):
        validate_transition(current, target, None)
