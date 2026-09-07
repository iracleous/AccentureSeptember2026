"""
example 21
langfuse-tracing
"""
import os
from typing import TypedDict

from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langfuse.langchain import CallbackHandler
from langgraph.graph import END, START, StateGraph


load_dotenv()

llm = AzureChatOpenAI( 
    model=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
)


class State(TypedDict):
    ticket: str
    category: str | None
    reply: str | None


def classify(state: State) -> dict:
    """Classify ticket by category."""
    return {
        "category": llm.invoke(
            f"One word category (billing/bug/general): {state['ticket']!r}"
        ).content.strip()
    }


def reply(state: State) -> dict:
    """Draft a reply based on category."""
    prompt = (
        f"Write a short reply to this {state['category']} ticket: {state['ticket']!r}"
    )
    return {"reply": llm.invoke(prompt).content}


graph = StateGraph(State)
graph.add_node("classify", classify)
graph.add_node("reply", reply)
graph.add_edge(START, "classify")
graph.add_edge("classify", "reply")
graph.add_edge("reply", END)
app = graph.compile()   

app.get_graph().draw_mermaid_png(output_file_path="graph-langfuse.png")

langfuse_handler = CallbackHandler()
result = app.invoke(
    {
        "ticket": "Payment failed twice", "category": None, 
    "reply": None
    },
    config={"callbacks": [langfuse_handler]},
)
print(result["reply"])