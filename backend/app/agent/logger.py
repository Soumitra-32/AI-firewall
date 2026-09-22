"""
Very small structured logger for Stage 1.

We're not touching PostgreSQL until Stage 2 — that's deliberate. Stage 1
just needs to prove *that* logging happens for every agent action; Stage 2
will swap this print-based logger for one that writes to the database
without changing how the agent calls it.
"""

import json
from datetime import datetime, timezone


def log_event(event_type: str, **details):
    """Print a structured JSON log line for a single agent event.

    event_type examples: 'user_message', 'tool_call', 'tool_result', 'agent_response'
    """
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event_type": event_type,
        **details,
    }
    print(json.dumps(entry))