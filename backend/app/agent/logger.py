"""
Stage 2 logger: same log_event() signature as Stage 1, but now writes
to PostgreSQL instead of just printing. agent.py does not need to change
at all — that's the point of keeping the interface stable across stages.

Still prints to console too, so you can watch it live while it's also
being saved.
"""

import sys
import os
import json
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.database import get_session, init_db
from database.models import Event

# Ensure tables exist the first time this module is imported.
init_db()


def log_event(event_type: str, session_id: str = "default", **details):
    """Persist a structured event to Postgres and also print it, so you
    can watch the agent live while everything is being saved."""

    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event_type": event_type,
        "session_id": session_id,
        **details,
    }
    print(json.dumps(entry))

    session = get_session()
    try:
        event = Event(
            event_type=event_type,
            session_id=session_id,
            tool_name=details.get("tool_name"),
            content=details.get("content"),
            tool_args=details.get("tool_args"),
        )
        session.add(event)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"[logger] failed to persist event: {e}")
    finally:
        session.close()