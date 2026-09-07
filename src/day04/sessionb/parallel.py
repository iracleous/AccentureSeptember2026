# Parallel processing: fan-out to 3 checks, wait for all, then combine results.
# Each check is independent and runs concurrently.

import operator
from typing import Annotated, TypedDict

from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langgraph.graph import END, START, StateGraph
import os

load_dotenv()

llm = AzureChatOpenAI(model=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"))


class State(TypedDict):
    ticket: str
    checks: Annotated[list[str], operator.add]
    verdict: str


def check_sentiment(state: State) -> dict:
    """Evaluate ticket sentiment."""
    result = llm.invoke(
        f"One word: is this ticket's tone angry or calm? {state['ticket']!r}"
    ).content.strip()
    return {"checks": [f"sentiment={result}"]}


def check_urgency(state: State) -> dict:
    """Evaluate ticket urgency."""
    result = llm.invoke(
        f"One word: is this ticket urgent or routine? {state['ticket']!r}"
    ).content.strip()
    return {"checks": [f"urgency={result}"]}


def check_category(state: State) -> dict:
    """Classify ticket category."""
    result = llm.invoke(
        f"One word category (billing/bug/general): {state['ticket']!r}"
    ).content.strip()
    return {"checks": [f"category={result}"]}


def combine(state: State) -> dict:
    """Combine parallel check results into a verdict."""
    return {"verdict": f"Ticket needs review: {', '.join(sorted(state['checks']))}"}


graph = StateGraph(State)
graph.add_node("check_sentiment", check_sentiment)
graph.add_node("check_urgency", check_urgency)
graph.add_node("check_category", check_category)
graph.add_node("combine", combine)

# Fan-out: 3 edges from START run all 3 nodes concurrently, not sequentially.
graph.add_edge(START, "check_sentiment")
graph.add_edge(START, "check_urgency")
graph.add_edge(START, "check_category")

# Fan-in: "combine" only runs once ALL 3 branches have finished.
graph.add_edge("check_sentiment", "combine")
graph.add_edge("check_urgency", "combine")
graph.add_edge("check_category", "combine")
graph.add_edge("combine", END)
app = graph.compile()

result = app.invoke(
    {
        "ticket": "This is the THIRD time you've double-charged me!!",
        "checks": [],
        "verdict": "",
    }
)


app.get_graph().draw_mermaid_png(output_file_path="graph-parallel.png")

print(result["verdict"])
