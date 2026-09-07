"""
tools
"""


import os

from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage

load_dotenv()

llm = AzureChatOpenAI( 
    model=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
)

@tool
def get_weather(location: str) -> dict:
    """Get the weather for a given location."""
    return {"location": location, "temperature": 20, "description": "Sunny"}    

@tool
def get_ticket_cost(location: str) -> dict:
    """Get the ticket cost for a given location."""  
    return {"location":location, "cost":1.20}

tools_by_name  = {"get_weather": get_weather, "get_ticket_cost": get_ticket_cost}
llm_with_tools = llm.bind_tools([get_weather, get_ticket_cost])


messages = [HumanMessage("What is the price for a ticket to location of Athens. What is the weather there?" )]
response = llm_with_tools.invoke(messages)
 

# Step 3: If the model called a tool, execute it
messages.append(response)
if response.tool_calls:
    for index,call in enumerate(response.tool_calls):
        tool_name = response.tool_calls[index]["name"]
        tool_args = response.tool_calls[index]["args"]
        tool_result = tools_by_name[tool_name].invoke(tool_args)
        print("[Tool result]", tool_result)

    # # Step 4: Feed the result back to the model

        messages.append(
            ToolMessage(content=str(tool_result), 
                        tool_call_id=response.tool_calls[index]["id"])
        )

    # Let the model formulate the final answer
    final_response = llm_with_tools.invoke(messages)
    print("[Final answer]", final_response.content)