"""
Stage 1 agent: a minimal LangGraph ReAct-style agent, provider-agnostic
between Groq (free tier, default) and OpenAI (paid, optional),
using the tools in tools.py, with every step logged via logger.py.

Run this file directly to chat with the agent from the terminal:
    python agent.py

Design notes for later stages:
- Tool calls are not gatekept yet — intentional, this is our "no firewall"
  baseline (see Stage 5).
- LLM provider is chosen at build time via LLM_PROVIDER env var, so
  switching providers later is a config change, not a rewrite.
"""

import os
from dotenv import load_dotenv
from langgraph.prebuilt import create_react_agent

from tools import TOOLS
from logger import log_event

load_dotenv()

print("DATABASE_URL in use:", os.environ.get("DATABASE_URL"))

SYSTEM_PROMPT = (
    "You are a helpful assistant with access to a calculator and a file "
    "reader tool. Use tools when they are needed to answer the user's "
    "question accurately. Only use the tools provided; do not invent "
    "information."
)


def build_llm():
    provider = os.environ.get("LLM_PROVIDER", "groq").lower()

    if provider == "openai":
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            model=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
            api_key=os.environ.get("OPENAI_API_KEY"),
            temperature=0,
        )

    if provider == "groq":
        from langchain_groq import ChatGroq
        return ChatGroq(
            model=os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile"),
            api_key=os.environ.get("GROQ_API_KEY"),
            temperature=0,
        )

    raise ValueError(f"Unknown LLM_PROVIDER: {provider}")


def build_agent():
    llm = build_llm()
    agent = create_react_agent(llm, TOOLS, prompt=SYSTEM_PROMPT)
    return agent


def run_turn(agent, user_input: str):
    log_event("user_message", content=user_input)

    result = agent.invoke({"messages": [("user", user_input)]})

    for message in result["messages"]:
        msg_type = type(message).__name__
        tool_calls = getattr(message, "tool_calls", None)

        if tool_calls:
            for call in tool_calls:
                log_event(
                    "tool_call",
                    tool_name=call["name"],
                    tool_args=call["args"],
                )
        elif msg_type == "ToolMessage":
            log_event(
                "tool_result",
                tool_name=getattr(message, "name", "unknown"),
                content=message.content,
            )
        elif msg_type == "AIMessage" and message.content:
            log_event("agent_response", content=message.content)

    final_message = result["messages"][-1]
    return final_message.content


if __name__ == "__main__":
    provider = os.environ.get("LLM_PROVIDER", "groq")
    agent = build_agent()
    print(f"Stage 1 Agent ready (provider: {provider}). Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ("exit", "quit"):
            break
        if not user_input:
            continue

        response = run_turn(agent, user_input)
        print(f"\nAgent: {response}\n")