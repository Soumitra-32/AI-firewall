"""
Stage 5: the firewall itself.

check(tool_name, tool_args) -> (allow: bool, reason: str)

This is the ONE function every tool call must pass through before it
executes. It is plain Python — no LLM call, no ambiguity, fully
auditable. This is what makes it a firewall rather than just "asking the
model nicely to be careful."
"""

from .policies import ALWAYS_ALLOWED_TOOLS, RESTRICTED_TOOLS, EMAIL_WHITELIST


def check(tool_name: str, tool_args: dict) -> tuple[bool, str]:
    if tool_name in ALWAYS_ALLOWED_TOOLS:
        return True, "Tool is unrestricted."

    if tool_name == "database_query":
        # Policy: reading protected data is allowed by itself.
        return True, "database_query is allowed by policy."

    if tool_name == "send_email":
        recipient = (tool_args or {}).get("to", "").strip().lower()
        if recipient in EMAIL_WHITELIST:
            return True, f"Recipient '{recipient}' is whitelisted."
        return False, f"Recipient '{recipient}' is not on the approved whitelist."

    if tool_name in RESTRICTED_TOOLS:
        # Safety net: a restricted tool with no explicit rule above.
        return False, f"No policy rule matched for restricted tool '{tool_name}'."

    # Unknown tool, not explicitly allowed anywhere — deny by default.
    return False, f"Tool '{tool_name}' is not recognized by any policy."