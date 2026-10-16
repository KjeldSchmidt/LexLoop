"""auth roles, oauth accounts, and students

Revision ID: 0004_auth_accounts
Revises: 0003_course_fks
Create Date: 2026-10-16
"""

from typing import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0004_auth_accounts"
down_revision: str | Sequence[str] | None = "0003_course_fks"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "user",
        sa.Column(
            "role",
            sa.String(length=50),
            nullable=False,
            server_default="teacher",
        ),
    )
    op.alter_column("user", "role", server_default=None)

    op.create_table(
        "oauth_account",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("oauth_name", sa.String(length=100), nullable=False),
        sa.Column("access_token", sa.String(length=1024), nullable=False),
        sa.Column("expires_at", sa.Integer(), nullable=True),
        sa.Column("refresh_token", sa.String(length=1024), nullable=True),
        sa.Column("account_id", sa.String(length=320), nullable=False),
        sa.Column("account_email", sa.String(length=320), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"], ondelete="cascade"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_oauth_account_account_id"),
        "oauth_account",
        ["account_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_oauth_account_oauth_name"),
        "oauth_account",
        ["oauth_name"],
        unique=False,
    )

    op.create_table(
        "lexloop_students",
        sa.Column("uuid", sa.UUID(), nullable=False),
        sa.Column("username", sa.String(length=100), nullable=False),
        sa.Column("hashed_password", sa.String(length=1024), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_by_teacher_id", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(
            ["created_by_teacher_id"],
            ["user.id"],
            name="student_teacher_fk",
        ),
        sa.PrimaryKeyConstraint("uuid"),
        sa.UniqueConstraint("username"),
    )


def downgrade() -> None:
    op.drop_table("lexloop_students")
    op.drop_index(
        op.f("ix_oauth_account_oauth_name"), table_name="oauth_account"
    )
    op.drop_index(
        op.f("ix_oauth_account_account_id"), table_name="oauth_account"
    )
    op.drop_table("oauth_account")
    op.drop_column("user", "role")
