"""Create the Phase 2 operational domain and seed reference data."""

from collections.abc import Sequence
from datetime import UTC, datetime
from typing import cast
from uuid import UUID

from alembic import op
from incident_api.districts import DISTRICT_SEEDS, ROLE_SEEDS
from incident_api.orm import ApplicationRoleRow, DistrictRow, IncidentRow  # noqa: F401
from lankarescue_database import Base
from sqlalchemy import Table

revision: str = "20260820_0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

ROLE_IDS = (
    UUID("10000000-0000-0000-0000-000000000001"),
    UUID("10000000-0000-0000-0000-000000000002"),
    UUID("10000000-0000-0000-0000-000000000003"),
    UUID("10000000-0000-0000-0000-000000000004"),
)
DEMO_INCIDENT_ID = UUID("20000000-0000-0000-0000-000000000001")


def upgrade() -> None:
    bind = op.get_bind()
    Base.metadata.create_all(bind=bind, checkfirst=False)
    op.bulk_insert(
        cast(Table, DistrictRow.__table__),
        [
            {"code": code, "name": name, "province": province}
            for code, name, province in DISTRICT_SEEDS
        ],
    )
    op.bulk_insert(
        cast(Table, ApplicationRoleRow.__table__),
        [
            {"id": role_id, "name": name, "description": description}
            for role_id, (name, description) in zip(ROLE_IDS, ROLE_SEEDS, strict=True)
        ],
    )
    now = datetime.now(UTC)
    op.bulk_insert(
        cast(Table, IncidentRow.__table__),
        [
            {
                "id": DEMO_INCIDENT_ID,
                "name": "Local Development Incident",
                "incident_type": "portfolio-demo",
                "status": "active",
                "starts_at": now,
                "ends_at": None,
                "created_at": now,
                "updated_at": now,
            }
        ],
    )


def downgrade() -> None:
    Base.metadata.drop_all(bind=op.get_bind(), checkfirst=False)
