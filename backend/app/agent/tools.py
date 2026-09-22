"""
Stage 1 tools.

These are intentionally simple, *simulated* tools. They don't touch real
systems yet — that's the point. Stage 1 proves the agent loop
(LLM -> decides to call a tool -> tool executes -> result goes back to LLM)
works end to end, with every call logged.

Later stages will route these calls through the firewall before execution.
For now, calls go straight through so we have a clean "before firewall"
baseline to compare against in Stage 4/5.
"""

from langchain_core.tools import tool

# A tiny fake filesystem so "file reading" is demonstrable without
# touching the real disk. Keys are the "filenames" the agent can request.
FAKE_FILES = {
    "notes.txt": "Meeting notes: discuss Q3 roadmap and budget planning.",
    "readme.txt": "This is a simulated file used for Stage 1 agent testing.",
}


@tool
def calculator(expression: str) -> str:
    """Evaluate a basic arithmetic expression, e.g. '2 + 2' or '(10 * 4) / 2'.
    Only numbers and + - * / ( ) . are allowed."""
    allowed_chars = set("0123456789+-*/(). ")
    if not set(expression) <= allowed_chars:
        return "Error: expression contains disallowed characters."
    try:
        # eval is safe here only because we've whitelisted the character set above.
        result = eval(expression, {"__builtins__": {}}, {})
        return str(result)
    except Exception as e:
        return f"Error: could not evaluate expression ({e})"


@tool
def file_reader(filename: str) -> str:
    """Read the contents of a simulated file by name (e.g. 'notes.txt')."""
    if filename in FAKE_FILES:
        return FAKE_FILES[filename]
    return f"Error: file '{filename}' not found."


TOOLS = [calculator, file_reader]