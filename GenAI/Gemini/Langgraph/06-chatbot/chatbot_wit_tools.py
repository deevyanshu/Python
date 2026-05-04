from typing import TypedDict, Annotated
from langgraph.graph import add_messages, StateGraph, END
from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq
from langchain_core.messages import AIMessage, HumanMessage
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import ToolNode

load_dotenv()

GROQ_API_KEY=os.getenv("GROQ_API_KEY")

tavily_tool=TavilySearchResults()

os.environ["GROQ_API_KEY"]=GROQ_API_KEY

tools=[tavily_tool]

llm=ChatGroq(model="llama-3.1-8b-instant")

llm_with_tools=llm.bind_tools(tools=tools)

class BasicChatState(TypedDict):
    messages: Annotated[list, add_messages]

def chatbot(state:BasicChatState):
    return {
        "messages": [llm_with_tools.invoke(state["messages"])]
    }

def tools_router(state: BasicChatState):
    last_messages=state["messages"][-1]

    if (hasattr(last_messages,"tool_calls") and len(last_messages.tool_calls)>0):
        return "tool_node"
    else:
        return END

tool_node=ToolNode(tools=tools)

graph=StateGraph(BasicChatState)

graph.add_node("chatbot", chatbot)
graph.add_node("tool_node",tool_node)

graph.set_entry_point("chatbot")
graph.add_conditional_edges("chatbot",tools_router)
graph.add_edge("tool_node","chatbot")

app=graph.compile()

while True:
    user_input= input("User: ")
    if(user_input in ["exit","end"]):
        break
    else:
        result=app.invoke(
            {
                "messages": [HumanMessage(content=user_input)]
            }
        )
    print("AI: ",result["messages"][-1].content)

