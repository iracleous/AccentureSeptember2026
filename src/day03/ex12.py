"""
Langgraph and tools

"""

import os
from typing import TypedDict, Literal, Annotated

from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langgraph.graph import END, START, StateGraph
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_core.tools import tool
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langgraph.types import Command




load_dotenv()

llm = AzureChatOpenAI( 
    model=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
)

class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


@tool
def get_ticket_count(status: str) -> int:
    """Return support ticket count by status."""
    return {"open": 42, "closed": 918}.get(status, 0)

tools = [get_ticket_count]
llm_with_tools = llm.bind_tools(tools)


def agent(state: State) -> Command[Literal["tools", "__end__"]]:
    """Decide whether to call tools or end the conversation."""
    ai_msg = llm_with_tools.invoke(state["messages"])
    goto = "tools" if ai_msg.tool_calls else END
    return Command(goto=goto, update={"messages": [ai_msg]})


graph = StateGraph(State)


graph.add_node("agent", agent)
graph.add_node("tools", ToolNode(tools))  # no hand-written loop -- ToolNode does it

graph.add_edge(START, "agent")
graph.add_edge("tools", "agent")

app = graph.compile()

app.get_graph().draw_mermaid_png(output_file_path="graph.png")

result = app.invoke(
    {"messages": [HumanMessage("How many open tickets does CodeHub have?")]}
)

print(result["messages"][-1].content)