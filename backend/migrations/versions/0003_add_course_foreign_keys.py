"""add course foreign keys on nodes, tags, and links

Revision ID: 0003_course_fks
Revises: aa13055e5739
Create Date: 2026-10-14

Migration 0002 added course_uuid columns without ForeignKeyConstraint.
ORM models already declare these FKs; this brings Alembic schema in line.
"""

from typing import Sequence

from alembic import op


revision: str = "0003_course_fks"
down_revision: str | Sequence[str] | None = "aa13055e5739"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Add course_uuid foreign keys matching the ORM."""
    op.create_foreign_key(
        "node_course_fk",
        "lexloop_nodes",
        "lexloop_courses",
        ["course_uuid"],
        ["uuid"],
    )
    op.create_foreign_key(
        "tag_course_fk",
        "lexloop_tags",
        "lexloop_courses",
        ["course_uuid"],
        ["uuid"],
    )
    op.create_foreign_key(
        "link_course_fk",
        "lexloop_links",
        "lexloop_courses",
        ["course_uuid"],
        ["uuid"],
    )


def downgrade() -> None:
    """Drop course_uuid foreign keys."""
    op.drop_constraint("link_course_fk", "lexloop_links", type_="foreignkey")
    op.drop_constraint("tag_course_fk", "lexloop_tags", type_="foreignkey")
    op.drop_constraint("node_course_fk", "lexloop_nodes", type_="foreignkey")
