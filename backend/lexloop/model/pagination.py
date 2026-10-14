"""Shared offset/limit pagination types."""

from __future__ import annotations

from typing import Generic, TypeVar

from fastapi import Query
from pydantic import BaseModel, Field

T = TypeVar("T")

DEFAULT_LIMIT = 50
MAX_LIMIT = 100


class Page(BaseModel, Generic[T]):  # type: ignore[explicit-any]
    """One page of results plus enough metadata for clients to fetch more."""

    items: list[T]
    total: int = Field(description="Total matching rows across all pages")
    offset: int
    limit: int


class PaginationParams(BaseModel):  # type: ignore[explicit-any]
    offset: int
    limit: int


def pagination_params(
    offset: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(
        DEFAULT_LIMIT,
        ge=1,
        le=MAX_LIMIT,
        description=f"Page size (max {MAX_LIMIT})",
    ),
) -> PaginationParams:
    """FastAPI dependency for list endpoints."""
    return PaginationParams(offset=offset, limit=limit)
