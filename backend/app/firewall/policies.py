"""
Stage 5: firewall policy definitions.

Policy choice for this version (deliberate, not automatic):
- database_query is ALLOWED — reading protected data isn't itself the
  harm; it's *where the data goes afterward* that matters.
- send_email is only ALLOWED if the recipient is on an explicit
  whitelist. Anything else — including plausible-looking external
  addresses — is BLOCKED, regardless of what the agent's reasoning was
  or how it was framed by the user.

This intentionally does NOT try to be clever about detecting "suspicious"
emails via keywords or heuristics. A static whitelist is dumb but
reliable — which is exactly the point of a rule-based firewall per the
project's core principle: the AI's judgment is not the security boundary.
"""

# Only these recipients are allowed to receive emails via send_email.
# In a real system this would come from a config file or admin UI;
# hardcoded here for Stage 5 simplicity.
EMAIL_WHITELIST = {
    "ceo@internal-company.example",
    "finance@internal-company.example",
}

# Tools that are always allowed with no restriction.
ALWAYS_ALLOWED_TOOLS = {"calculator", "file_reader", "web_search"}

# Tools that require a policy check before execution.
RESTRICTED_TOOLS = {"database_query", "send_email"}