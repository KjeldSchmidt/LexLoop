"""add-courses

Revision ID: aa13055e5739
Revises: b85ae5afb4e9
Create Date: 2026-02-05 20:15:55.302272

"""

import uuid
from typing import Sequence

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "aa13055e5739"
down_revision: str | Sequence[str] | None = "b85ae5afb4e9"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    courses_table = op.create_table(
        "lexloop_courses",
        sa.Column("uuid", sa.UUID(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint("uuid"),
    )

    english_course_uuid = uuid.uuid4()
    op.execute(
        courses_table.insert().values(
            uuid=english_course_uuid, name="English Original"
        )
    )

    op.add_column(
        "lexloop_nodes",
        sa.Column(
            "course_uuid",
            sa.UUID(),
            nullable=False,
            server_default=str(english_course_uuid),
        ),
    )
    op.alter_column("lexloop_nodes", "course_uuid", server_default=None)

    op.add_column(
        "lexloop_tags",
        sa.Column(
            "course_uuid",
            sa.UUID(),
            nullable=False,
            server_default=str(english_course_uuid),
        ),
    )
    op.alter_column("lexloop_tags", "course_uuid", server_default=None)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("lexloop_tags", "course_uuid")
    op.drop_column("lexloop_nodes", "course_uuid")
    op.drop_table("lexloop_courses")
