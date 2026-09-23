"""
Stage 2 models: just enough to persist agent activity.
Attacks, firewall decisions, and evaluation results get their own
columns/tables in later stages — kept minimal here on purpose.
"""

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON

from .database import Base


class Event(Base):
    """One row per logged agent event (user message, tool call, tool
    result, or agent response). This is the same shape Stage 1's
    log_event() printed to console — now it's a durable row instead."""

    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    event_type = Column(String, nullable=False)   # user_message | tool_call | tool_result | agent_response
    tool_name = Column(String, nullable=True)
    content = Column(Text, nullable=True)
    tool_args = Column(JSON, nullable=True)
    session_id = Column(String, nullable=True)     # ties events to one conversation/run