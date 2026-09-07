"""
Langgraph and routing

"""

import os
from typing import TypedDict, Literal

from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command


load_dotenv()

llm = AzureChatOpenAI( 
    model=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
)

class State(TypedDict):
    ticket: str
    category: str | None
    reply: str | None

def classify(state: State) -> Command[Literal[
    "billing", "bug", "general"]]:
    """Classify ticket into a category for routing."""
    category = (
        llm.invoke(
            f"Classify this support ticket as exactly one word -- billing, bug, or general: {state['ticket']!r}"
        )
        .content.strip()
        .lower()
    )

    category = category if category in ("billing", "bug", "general") else "general"
    return Command(goto=category, update={"category": category}) 

def billing(state: State) -> dict:
    """Handle billing-related support tickets."""
    return {
        "reply": llm.invoke(
            f"Write a short billing-support reply to: {state['ticket']!r}"
        ).content
    }

def bug(state: State) -> dict:
    """Handle bug report support tickets."""
    return {
        "reply": llm.invoke(
            f"Write a short reply acknowledging this bug report: {state['ticket']!r}"
        ).content
    }


def general(state: State) -> dict:
    """Handle general support tickets."""
    return {
        "reply": llm.invoke(
            f"Write a short general support reply to: {state['ticket']!r}"
        ).content
    }

 



graph = StateGraph(State)

graph.add_node("classify", classify)
graph.add_node("billing", billing)
graph.add_node("bug", bug)
graph.add_node("general", general)



graph.add_edge(START, "classify")
graph.add_edge("billing", END)
graph.add_edge("bug", END)
graph.add_edge("general", END)

app = graph.compile()

app.get_graph().draw_mermaid_png(output_file_path="graph.png")

result = app.invoke(
    {"ticket": "I was charged twice this month", 
    #  "category": None, 
    #  "reply": None
     }
)
print(f"[{result['category']}]", result["reply"])