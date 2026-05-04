from typing import TypedDict, Annotated, Optional
from langgraph.graph import add_messages, StateGraph, END
from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq
from langgraph.prebuilt import ToolNode
from langchain_community.tools.tavily_search import TavilySearchResults
import asyncio
from langgraph.checkpoint.memory import MemorySaver
from uuid import uuid4
import json
from langchain_core.messages import HumanMessage

load_dotenv()

GROQ_API_KEY=os.getenv("GROQ_API_KEY")

os.environ["GROQ_API_KEY"]=GROQ_API_KEY

llm=ChatGroq(model="llama-3.3-70b-versatile")

tavily_search=TavilySearchResults(max_results=2)

tools=[tavily_search]

memory=MemorySaver()

llm_with_tools=llm.bind_tools(tools=tools)

class State(TypedDict):
    messages:Annotated[list,add_messages]

async def model(state:State):
    result=await llm_with_tools.ainvoke(state["messages"])  
    return {
        "messages":[result]
    }

async def tools_router(state:State):
    last_message=state["messages"][-1]

    if(hasattr(last_message,"tool_calls") and len(last_message.tool_calls)>0):
        return "tool_node"
    else:
        return END

tool_node=ToolNode(tools=tools)

graph=StateGraph(State)

graph.add_node("model",model)
graph.add_node("tool_node",tool_node)
graph.set_entry_point("model")
graph.add_conditional_edges("model",tools_router)
graph.add_edge("tool_node","model")

app=graph.compile(checkpointer=memory)

config={
    "configurable": {
        "thread_id":2
    }
}

events=app.astream_events({
    "messages":HumanMessage(content="write 100 words essay on 'What is LangGraph?")
},config=config, version="v2")

async def main():
    async for event in events:
        if (event["event"]=="on_chain_stream" and event["name"]=="model"):
            messages=event["data"]["chunk"].get("messages",[])

            if messages:
                print(messages[0].content,flush=True)

if __name__ == "__main__":
    asyncio.run(main())    