"""Generate unique 4-letter uppercase course signup codes."""

from __future__ import annotations

import random
import string

from sqlalchemy.orm import Session

from lexloop.repository import course_repository

_LETTERS = string.ascii_uppercase
_MAX_ATTEMPTS = 64


def generate_signup_code(session: Session) -> str:
    """Return a unique 4-character A–Z code not used by any course."""
    for _ in range(_MAX_ATTEMPTS):
        candidate = "".join(random.choices(_LETTERS, k=4))
        if course_repository.get_by_signup_code(candidate, session) is None:
            return candidate
    raise RuntimeError("SIGNUP_CODE_GENERATION_FAILED")


def normalize_signup_code(code: str) -> str:
    return code.strip().upper()
