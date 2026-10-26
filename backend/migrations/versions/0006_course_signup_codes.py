"""course signup codes and enrollment requests

Revision ID: 0006_signup_codes
Revises: 0005_course_own
Create Date: 2026-10-26
"""

from __future__ import annotations

import random
import string
from typing import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0006_signup_codes"
down_revision: str | Sequence[str] | None = "0005_course_own"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_LETTERS = string.ascii_uppercase


def _unique_codes(count: int, existing: set[str]) -> list[str]:
    codes: list[str] = []
    used = set(existing)
    while len(codes) < count:
        candidate = "".join(random.choices(_LETTERS, k=4))
        if candidate in used:
            continue
        used.add(candidate)
        codes.append(candidate)
    return codes


def upgrade() -> None:
    op.add_column(
        "lexloop_courses",
        sa.Column("signup_code", sa.String(length=4), nullable=True),
    )

    bind = op.get_bind()
    rows = bind.execute(sa.text("SELECT uuid FROM lexloop_courses")).fetchall()
    codes = _unique_codes(len(rows), set())
    for row, code in zip(rows, codes, strict=True):
        bind.execute(
            sa.text(
                "UPDATE lexloop_courses SET signup_code = :code WHERE uuid = :uuid"
            ),
            {"code": code, "uuid": row[0]},
        )

    op.alter_column("lexloop_courses", "signup_code", nullable=False)
    op.create_unique_constraint(
        "course_signup_code_uq", "lexloop_courses", ["signup_code"]
    )

    op.create_table(
        "lexloop_course_enrollment_requests",
        sa.Column("course_uuid", sa.UUID(), nullable=False),
        sa.Column("student_uuid", sa.UUID(), nullable=False),
        sa.Column(
            "requested_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["course_uuid"],
            ["lexloop_courses.uuid"],
            name="join_request_course_fk",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["student_uuid"],
            ["lexloop_students.uuid"],
            name="join_request_student_fk",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("course_uuid", "student_uuid"),
    )


def downgrade() -> None:
    op.drop_table("lexloop_course_enrollment_requests")
    op.drop_constraint(
        "course_signup_code_uq", "lexloop_courses", type_="unique"
    )
    op.drop_column("lexloop_courses", "signup_code")
