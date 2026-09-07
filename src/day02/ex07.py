"""
Author: Dimitrios  


"""


import os

from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser

load_dotenv()

llm = AzureChatOpenAI( 
    model=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "{system}"),
        ("human" , "{question}"),
    ]
)
message = prompt.invoke ({"question": "What is AI?",
"system":"answer in 5 paragraphs."}
 )

response = llm.invoke(message)
print("Model:", llm.model)
print("Response:", response.content)

print("80")
chain = prompt | llm | JsonOutputParser()

try:    
    result = chain.invoke(
    {
        "question":" what is the weather today?",
        "system": "Be a weather forecaster"
        }
 )

    print (result)
except:
    print("parsing error")