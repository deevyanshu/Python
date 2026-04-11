import os
from dotenv import load_dotenv
# from google import genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

os.environ['GEMINI_API_KEY']=GEMINI_API_KEY

@tool
def get_weather(location:str):
    """Consult this tool to get the current weather for a specific city."""
    if "Indore" in location:
        return "It's 32°C and sunny in Indore."
    return f"The weather in {location} is pleasant, approximately 25°C."

tools = [get_weather]

llm=ChatGoogleGenerativeAI(
    model="gemini-3-flash-preview",
    max_retries=6
)

llm_with_tools=llm.bind_tools(tools)

response=llm_with_tools.invoke("What is weather in indore")

print(response.tool_calls)

# for tool_call in response.tool_calls:
#     selected_tool={"get_weather": get_weather}[tool_call['name']]
#     tool_ouput=selected_tool.invoke(tool_call['args'])
#     print(f"Tool Output: {tool_ouput}")