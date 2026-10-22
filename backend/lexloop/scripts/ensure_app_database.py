"""Ensure the application database exists on the shared tck-labs RDS.

Connects to the bootstrap DB ``tcklabs`` using credentials derived from
``DB_URL`` (which points at ``lexloop_{env}``), then ``CREATE DATABASE`` if
needed. Safe to run repeatedly before Alembic migrations.
"""

from __future__ import annotations

import os
import sys
from urllib.parse import urlparse, urlunparse

import psycopg


def _admin_url_and_app_db(app_url: str) -> tuple[str, str]:
    parsed = urlparse(app_url)
    app_db = (parsed.path or "/").lstrip("/")
    if not app_db:
        raise SystemExit(
            "DB_URL path must include the application database name"
        )
    # psycopg accepts postgresql://; strip SQLAlchemy driver suffix if present.
    scheme = "postgresql"
    admin = parsed._replace(scheme=scheme, path="/tcklabs")
    return urlunparse(admin), app_db


def main() -> None:
    app_url = os.environ.get("DB_URL", "").strip()
    if not app_url:
        raise SystemExit("DB_URL is not set")

    admin_url, app_db = _admin_url_and_app_db(app_url)
    # Expect {project}_{env} — lowercase letters, digits, underscores only.
    if not app_db.replace("_", "").isalnum() or app_db != app_db.lower():
        raise SystemExit(f"Refusing unsafe database name: {app_db!r}")

    with psycopg.connect(admin_url, autocommit=True) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT 1 FROM pg_database WHERE datname = %s", (app_db,)
            )
            if cur.fetchone() is not None:
                print(f"Database {app_db} already exists")
                return
            cur.execute(f'CREATE DATABASE "{app_db}"')
            print(f"Created database {app_db}")


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as exc:  # noqa: BLE001 — CLI entrypoint
        print(f"ensure_app_database failed: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
