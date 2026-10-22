"""course ownership, description, and enrollments

Revision ID: 0005_course_own
Revises: 0004_auth_accounts
Create Date: 2026-10-22
"""

from typing import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0005_course_own"
down_revision: str | Sequence[str] | None = "0004_auth_accounts"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "lexloop_courses",
        sa.Column(
            "description",
            sa.Text(),
            nullable=False,
            server_default="",
        ),
    )
    op.alter_column("lexloop_courses", "description", server_default=None)

    op.add_column(
        "lexloop_courses",
        sa.Column("owner_teacher_id", sa.UUID(), nullable=True),
    )
    op.create_foreign_key(
        "course_owner_teacher_fk",
        "lexloop_courses",
        "user",
        ["owner_teacher_id"],
        ["id"],
    )

    op.create_table(
        "lexloop_course_enrollments",
        sa.Column("course_uuid", sa.UUID(), nullable=False),
        sa.Column("student_uuid", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(
            ["course_uuid"],
            ["lexloop_courses.uuid"],
            name="enrollment_course_fk",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["student_uuid"],
            ["lexloop_students.uuid"],
            name="enrollment_student_fk",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("course_uuid", "student_uuid"),
    )


def downgrade() -> None:
    op.drop_table("lexloop_course_enrollments")
    op.drop_constraint(
        "course_owner_teacher_fk", "lexloop_courses", type_="foreignkey"
    )
    op.drop_column("lexloop_courses", "owner_teacher_id")
    op.drop_column("lexloop_courses", "description")
