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
from fastapi import FastAPI,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import StreamingResponse
from langchain_core.messages import AIMessage

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

app_builder=graph.compile(checkpointer=memory)

fast_app=FastAPI()

fast_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
    expose_headers=["Content-Type"]
)

def serialise_ai_message_chunk(chunk):
    if(isinstance(chunk,AIMessage)):
        return chunk.content
    else:
        raise TypeError(
            f"Object of type {type(chunk)} is not serialisable as an AIMessageChunk."
        )
    
async def generate_chat_responses(messages:str, checkpoint_id:Optional[str]=None):
    is_new_conversation=checkpoint_id is None

    if(is_new_conversation):
        #generate a new checkpoint id for the conversation
        new_checkpoint_id=str(uuid4())
        
        config={
            "configurable": {
                "thread_id": new_checkpoint_id
            }
        }

        events=app_builder.astream_events({
            "messages": [HumanMessage(content=messages)]
        },version="v2", config=config)

        #first send the checkpoint id
        yield f"data: {{\"type\":\"checkpoint\",\"checkpoint_id\":\"{new_checkpoint_id}\"}}\n\n"
    else:
        config={
            "configurable": {
                "thread_id": checkpoint_id
            }
        }

        events=app_builder.astream_events(
            {"messages": [HumanMessage(content=messages)]},
            version="v2", config=config)
    
    async for event in events:
        event_type=event["event"]

        if (event_type=="on_chain_stream"and event["name"]=="model"):
            ai_message=event["data"]["chunk"].get("messages",[])
            chunk_content=serialise_ai_message_chunk(ai_message[0])

            safe_content=chunk_content.replace("'","\\'").replace("\n","\\n")
            # yield f"data: {{\"type\":\"content\",\"content\":\"{safe_content}\"}}\n\n"
            yield f"data: {json.dumps({'type': 'content', 'content': chunk_content})}\n\n"
        elif event_type=="on_tool_start" and event["name"]=="tavily_search_results_json":
            #check if there are any tool calls
            # tool=event["data"]["output"].get(messages,[])
            # if tool:
            #     tool_calls=tool[0].get("tool_calls",[]) 
            #     search_calls=[call for call in tool_calls if call["name"]=="tavily_search_results_json"]

            #     if(search_calls):
            #         search_query=search_calls[0]["args"].get("query","")
            #         safe_query=search_query.replace('"','\\"').replace("'","\\'").replace("\n","\\n")
                    search_query = event['data']['input'].get('query')
                    safe_query=search_query.replace('"','\\"').replace("'","\\'").replace("\n","\\n")
                    # yield f"data: {{\"type\":\"search_start\",\"query\":\"{safe_query}\"}}\n\n"
                    yield f"data: {json.dumps({'type': 'search_start', 'query': search_query})}\n\n"
        elif event_type=="on_tool_end" and event["name"]=="tavily_search_results_json":
            output=event["data"]["output"].content
            # if(isinstance(output,list)):
            #     urls=[]

            #     for item in output:
            #         url=item.get("url","")
            #         urls.append(url)
                
            #     urls_json=json.dumps(urls)
            #     yield f"data: {{\"type\":\"search_results\",\"urls\":{urls_json}}}\n\n"
            data = json.loads(output)
            urls=[]
            for item in data:
                url = item.get("url", "")
                urls.append(url)
            urls_json=json.dumps(urls)
            # yield f"data: {{\"type\":\"search_results\",\"urls\":{urls_json}}}\n\n"
            yield f"data: {json.dumps({'type': 'search_results', 'urls': urls})}\n\n"
    
    yield f"data: {{\"type\":\"end\"}}\n\n"

#yield is used for server side events to send data to the client in chunks as it becomes available. Each chunk of data is sent as a separate event, allowing the client to process it incrementally without waiting for the entire response to be generated.
            
@fast_app.get("/")
def root():
    return {"message":"Hello World"}

@fast_app.get("/chat_stream/{messages}")
async def chat_stream(messages:str,checkpoint_id:Optional[str]=None):
    return StreamingResponse(
        generate_chat_responses(messages,checkpoint_id),
        media_type="text/event-stream"
    )