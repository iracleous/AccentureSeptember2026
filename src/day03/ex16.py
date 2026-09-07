# ReAct agent pattern

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.agents.middleware import ModelRetryMiddleware, ToolErrorMiddleware
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
import os
from langchain_openai import AzureChatOpenAI

load_dotenv()

llm = AzureChatOpenAI( 
    model=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
)

@tool
def get_ticket_priority(ticket_id: str) -> str:
    """Look up a CodeHub ticket's priority level."""
    return {"T-101": "critical", "T-102": "low"}.get(ticket_id, "medium")


@tool
def get_sla_hours(priority: str) -> int:
    """Look up the SLA response time (in hours) for a priority level: critical, high, medium, or low."""
    hours = {"critical": 1, "high": 4, "medium": 24, "low": 72}.get(priority.lower())
    if hours is None:
        raise ValueError(
            f"{priority!r} is not a known priority -- call get_ticket_priority first"
        )
    return hours


def on_tool_error(exc: Exception) -> str | None:
    """Turn a raised ValueError into an observation the agent can act on and
    retry from, instead of crashing the whole run -- this matters because a
    smaller model will sometimes guess at both tool calls in one turn instead
    of waiting for the first result."""
    if isinstance(exc, ValueError):
        return str(exc)
    return None  # anything else still propagates and halts the run


agent = create_agent(
    llm,
    tools=[get_ticket_priority, get_sla_hours] ,
    middleware=[ToolErrorMiddleware(on_tool_error), ModelRetryMiddleware()],
)

result = agent.invoke(
    {"messages": [HumanMessage("What's the SLA response time for ticket T-101?")]}
)
for msg in result["messages"]:
    print(f"[{msg.type}]", getattr(msg, "tool_calls", None) or msg.content)