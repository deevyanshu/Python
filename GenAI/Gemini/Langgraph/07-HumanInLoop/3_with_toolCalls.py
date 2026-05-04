from typing import TypedDict, Annotated
from langgraph.graph import add_messages, StateGraph, END
from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq
from langchain_core.messages import AIMessage, HumanMessage
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver


load_dotenv()
memory=MemorySaver()

GROQ_API_KEY=os.getenv("GROQ_API_KEY")

tavily_tool=TavilySearchResults()

os.environ["GROQ_API_KEY"]=GROQ_API_KEY

tools=[tavily_tool]

llm=ChatGroq(model="llama-3.3-70b-versatile")

llm_with_tools=llm.bind_tools(tools=tools)

class BasicState(TypedDict):
    messages: Annotated[list, add_messages]

def model(state:BasicState):
    return {
        "messages":[llm_with_tools.invoke(state["messages"])]
    }

def tools_router(state: BasicState):
    last_messages=state["messages"][-1]

    if (hasattr(last_messages,"tool_calls") and len(last_messages.tool_calls)>0):
        return "tools"
    else:
        return END

tool_node=ToolNode(tools=tools)

graph=StateGraph(BasicState)

graph.add_node("model", model)
graph.add_node("tools",tool_node)

graph.set_entry_point("model")
graph.add_conditional_edges("model",tools_router)
graph.add_edge("tools","model")

app=graph.compile(checkpointer=memory, interrupt_before=["tools"])

config={"configurable":
        {
           "thread_id":1 
        }}

events=app.stream({
    "messages":[HumanMessage("what is current weather in indore?")]
},config=config,stream_mode="values")

for event in events:
    event["messages"][-1].pretty_print()

events=app.stream(None,config,stream_mode="values")
for event in events:
    event["messages"][-1].pretty_print()