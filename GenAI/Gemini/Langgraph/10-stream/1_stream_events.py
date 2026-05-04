from typing import TypedDict, Annotated
from langgraph.graph import add_messages, StateGraph, END
from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq
from langgraph.prebuilt import ToolNode
from langchain_community.tools.tavily_search import TavilySearchResults
import asyncio

load_dotenv()

GROQ_API_KEY=os.getenv("GROQ_API_KEY")

os.environ["GROQ_API_KEY"]=GROQ_API_KEY

llm=ChatGroq(model="llama-3.3-70b-versatile")

tavily_search=TavilySearchResults(max_results=2)

tools=[tavily_search]

class AgentState(TypedDict):
    messages:Annotated[list,add_messages]

llm_with_tools=llm.bind_tools(tools=tools)

def model(state:AgentState):
    return {
        "messages":[llm_with_tools.invoke(state["messages"])]
    }

def tools_router(state:AgentState):
    last_message=state["messages"][-1]

    if(hasattr(last_message,"tool_calls") and len(last_message.tool_calls)>0):
        return "tool_node"
    else:
        return END

tool_node=ToolNode(tools=tools)

graph=StateGraph(AgentState)

graph.add_node("model",model)
graph.add_node("tool_node",tool_node)
graph.set_entry_point("model")
graph.add_conditional_edges("model",tools_router)
graph.add_edge("tool_node","model")
app=graph.compile()

# input={
#     "messages":["What is current weather in banglore"]
# }

# events=app.stream(input=input, stream_mode="updates")

# for event in events:
#     print(event)

input={
    "messages":"what is weather in indore"
}
events=app.astream_events(input=input,version="v2")

async def main():
    # Assuming 'events' is an asynchronous iterator
    async for event in events:
        print(event)

# async def main():
#     async for event in events:
#         if event["event"]=="on_chain_stream":
#             messages=event["data"]["chunk"].get("messages",[])

#             if messages:
#                 print(messages[0].content,end="",flush=True)

if __name__ == "__main__":
    asyncio.run(main())
