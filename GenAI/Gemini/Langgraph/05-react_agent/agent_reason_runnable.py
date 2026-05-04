from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

llm= ChatGoogleGenerativeAI(model="gemini-3-flash-preview",
    max_retries=6
)

@tool
def weather(city:str)->str:
    """get weather for a city"""
    return f"its sunny in {city}"

tools=[weather]

agent=create_agent(model=llm, tools=tools, system_prompt="You are a helpful assistant")

# response=agent.invoke({
#     "messages":[
#         {"role": "user", "content": "what is weather in banglore"}
#     ]
# })

# print(response["messages"][-1].content[0].get('text'))