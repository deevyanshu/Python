from typing import TypedDict,Annotated, Dict
from langgraph.graph import add_messages, StateGraph, END, START
from langchain_groq import ChatGroq
from langchain_core.messages import AIMessage, HumanMessage
from dotenv import load_dotenv
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import ToolNode
import os

load_dotenv()

GROQ_API_KEY=os.getenv("GROQ_API_KEY")

os.environ["GROQ_API_KEY"]=GROQ_API_KEY

class ChildState(TypedDict):
    messages: Annotated[list, add_messages]

search_tool=TavilySearchResults(max_results=2)
tools=[search_tool]

llm=ChatGroq(model="llama-3.3-70b-versatile")

llm_with_tools=llm.bind_tools(tools=tools)

def agent(state:ChildState):
    return {
        "messages":[llm_with_tools.invoke(state["messages"])]
    }

def tools_router(state:ChildState):
    last_message=state["messages"][-1]

    if(hasattr(last_message,"tool_calls") and len(last_message.tool_calls)>0):
        return "tool_node"
    else:
        return END

tool_node=ToolNode(tools=tools)

subgraph=StateGraph(ChildState)

subgraph.add_node("agent", agent)
subgraph.add_node("tool_node",tool_node)
subgraph.set_entry_point("agent")

subgraph.add_conditional_edges("agent",tools_router)
subgraph.add_edge("tool_node","agent")

search_app=subgraph.compile()

# response=search_app.invoke({
#     "messages": [HumanMessage(content="How is weather in chennai")]
# })
# print(response["messages"][-1].content)

#case 1: Shared Scheme(Direct Embedding)

class ParentState(TypedDict):
    messages:Annotated[list,add_messages]

parent_graph=StateGraph(ParentState)

parent_graph.add_node("search_agent", search_app)

parent_graph.add_edge(START, "search_agent")
parent_graph.add_edge("search_agent",END)

parent_app=parent_graph.compile()

result=parent_app.invoke({"messages": [HumanMessage(content="How is weather in indore")]})
print(result["messages"][-1].content)

#case 2: Different schema(invoke with transformation)

class QueryState(TypedDict):
    query:str
    response:str

def search_agent(state:QueryState)-> Dict:
    #Transform from parent schema to subgraph schema
    subgraph_input={
        "messages":[HumanMessage(content=state["query"])]
    }

    #invoke the subgraph
    subgraph_result=search_app.invoke(subgraph_input)

    #Trasform response back to parent schema
    assistant_message=subgraph_result["messages"][-1]
    return {"response": assistant_message.content}

parent_graph=StateGraph(QueryState)

parent_graph.add_node("search_agent",search_agent)

parent_graph.add_edge(START,"search_agent")
parent_graph.add_edge("search_agent",END)

parent_app=parent_graph.compile()

res=parent_app.invoke({
    "query":"How is weather in chennai",
    "response":""
})

print(res)


