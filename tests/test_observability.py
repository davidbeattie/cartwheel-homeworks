"""Authentication tests for the Cartwheel server endpoint (Homework 2, Part D).

These tests do not require Langfuse, Docker, or a model provider key.
They run entirely offline against the local SQLite database.
"""

from __future__ import annotations

import pytest
from fastapi import HTTPException

from server.app import SessionCreate, _SESSIONS, create_session, _authorize


def test_create_session_rejects_wrong_role() -> None:
    """Session creation must reject a user whose claimed role differs from the database."""
    # User 9002 is a merchant in the database. Claiming 'shopper' must fail.
    _SESSIONS.clear()
    with pytest.raises(HTTPException) as exc_info:
        create_session(SessionCreate(user_id=9002, role="shopper"))
    assert exc_info.value.status_code == 403


def test_token_from_one_session_cannot_authorize_another() -> None:
    """A token issued for session A must be rejected when used on session B."""
    _SESSIONS.clear()

    # Create two separate sessions.
    response_a = create_session(SessionCreate(user_id=1, role="shopper"))
    response_b = create_session(SessionCreate(user_id=9501, role="support"))

    session_id_a = response_a["session_id"]
    session_id_b = response_b["session_id"]
    token_a = response_a["token"]

    # Token from session A must not authorise session B.
    with pytest.raises(HTTPException) as exc_info:
        _authorize(session_id_b, f"Bearer {token_a}")
    assert exc_info.value.status_code == 403
