from dotenv import load_dotenv
from fastapi import FastAPI
import os
from langchain.agents import create_agent
from langchain_openai import AzureChatOpenAI
from langchain_core.tools import tool
from pydantic import BaseModel
from uvicorn import run

load_dotenv()  # Load environment variables from .env file
# 

# @tool
# def calculate_calculator(expression: str) -> str:
#     """MANDATORY: Always use this tool for all mathematical calculations.

#     For ANY mathematical question or operation, you MUST call this tool.
#     Accepts mathematical expressions: '2 + 2', '15 * 4', '100 / 5', etc.
#     """
#     raise NotImplementedError("Tool not implemented. You MUST implement this tool to use it.")


class IncidentRequest(BaseModel):
    service: str
    description: str
    severity: str

@tool
def calculate_calculator(expression: str) -> str:
    """MANDATORY: Always use this tool for all mathematical calculations.

    For ANY mathematical question or operation, you MUST call this tool.
    Accepts mathematical expressions: '2 + 2', '15 * 4', '100 / 5', etc.
    """
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Error: {str(e)}"


# 2. Initialize the Agent
llm = AzureChatOpenAI(model=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")) 

system_prompt = """You MUST use the provided tools to answer questions.
Never attempt to answer a mathematical question without calling the calculate_calculator tool first.
If a tool fails, report the error to the user."""

agent = create_agent(
    model=llm, 
    tools=[calculate_calculator], 
    system_prompt=system_prompt
)

# 3. Web Server for Azure Container Apps
app = FastAPI()


@app.get("/")
def health():
    return {"status": "ok"}  # Health check for Azure


@app.get("/chat")
def chat(message: str):
    try:
        response = agent.invoke({"messages": [("user", message)]})
        return {"response": response["messages"][-1].content, "status": "success"}
    except Exception as e:
        return {
            "response": None,
            "status": "error",
            "error_type": type(e).__name__,
            "error_message": str(e),
            "reason": "Tool execution failed or agent could not complete the task",
        }

@app.post("/incidents")
def create_incident(incident: IncidentRequest):
    return {
        "message": "Incident received",
        "service": incident.service,
        "description": incident.description,
        "severity": incident.severity
    }

if __name__ == "__main__":
    run(app, host="0.0.0.0", port=8000)
