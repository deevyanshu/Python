import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.documents import Document
from typing import Annotated, Literal, TypedDict, Sequence
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, END, START
from langchain_core.tools.retriever import create_retriever_tool
from langchain_core.tools import tool 
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

PINECONE_KEY= os.getenv("PINECONE_KEY")

os.environ["PINECONE_API_KEY"] = PINECONE_KEY
os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY

#initialize embeddings
embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001",
 output_dimensionality=768
)

#connect to Pinecone index
index_name="rag-index"
vectorstore=PineconeVectorStore(index_name=index_name, embedding=embeddings)

docs = [
    Document(
        page_content="Peak Performance Gym was founded in 2015 by former Olympic athlete Marcus Chen. With over 15 years of experience in professional athletics, Marcus established the gym to provide personalized fitness solutions for people of all levels. The gym spans 10,000 square feet and features state-of-the-art equipment.",
        metadata={"source": "about.txt"}
    ),
    Document(
        page_content="Peak Performance Gym is open Monday through Friday from 5:00 AM to 11:00 PM. On weekends, our hours are 7:00 AM to 9:00 PM. We remain closed on major national holidays. Members with Premium access can enter using their key cards 24/7, including holidays.",
        metadata={"source": "hours.txt"}
    ),
    Document(
        page_content="Our membership plans include: Basic (₹1,500/month) with access to gym floor and basic equipment; Standard (₹2,500/month) adds group classes and locker facilities; Premium (₹4,000/month) includes 24/7 access, personal training sessions, and spa facilities. We offer student and senior citizen discounts of 15% on all plans. Corporate partnerships are available for companies with 10+ employees joining.",
        metadata={"source": "membership.txt"}
    ),
    Document(
        page_content="Group fitness classes at Peak Performance Gym include Yoga (beginner, intermediate, advanced), HIIT, Zumba, Spin Cycling, CrossFit, and Pilates. Beginner classes are held every Monday and Wednesday at 6:00 PM. Intermediate and advanced classes are scheduled throughout the week. The full schedule is available on our mobile app or at the reception desk.",
        metadata={"source": "classes.txt"}
    ),
    Document(
        page_content="Personal trainers at Peak Performance Gym are all certified professionals with minimum 5 years of experience. Each new member receives a complimentary fitness assessment and one free session with a trainer. Our head trainer, Neha Kapoor, specializes in rehabilitation fitness and sports-specific training. Personal training sessions can be booked individually (₹800/session) or in packages of 10 (₹7,000) or 20 (₹13,000).",
        metadata={"source": "trainers.txt"}
    ),
    Document(
        page_content="Peak Performance Gym's facilities include a cardio zone with 30+ machines, strength training area, functional fitness space, dedicated yoga studio, spin class room, swimming pool (25m), sauna and steam rooms, juice bar, and locker rooms with shower facilities. Our equipment is replaced or upgraded every 3 years to ensure members have access to the latest fitness technology.",
        metadata={"source": "facilities.txt"}
    )
]

# text_splitter= RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
# texts=text_splitter.split_documents(docs)

# #upload to pineconce
# vectorstore.add_documents(texts)

model=ChatGoogleGenerativeAI(
    model="gemini-3-flash-preview",
    max_retries=6
)

#setup the retriever
retriever=vectorstore.as_retriever(search_kwargs={"k":3}
) #get top 3 results

retriever_tool = create_retriever_tool(
    retriever,
    "retriever_tool",
    "Information related to Gym History & Founder, Operating Hours, Membership Plans, Fitness Classes, Personal Trainers, and Facilities & Equipment of Peak Performance Gym",
)

@tool
def off_topic():
    """Catch all Questions NOT related to Peak Performance Gym's history, hours, membership plans, fitness classes, trainers, or facilities"""
    return "Forbidden - do not respond to the user"

tools=[retriever_tool, off_topic]

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

def agent(state:AgentState):
    messages=state["messages"]
    llm=model.bind_tools(tools)
    response=llm.invoke(messages)
    return {"messages": [response]}

def should_continue(state:AgentState)-> Literal["tools", "__end__"]:
    last_message=state["messages"][-1]
    if last_message.tool_calls:
        return "tools"
    return END

workflow = StateGraph(AgentState)

workflow.add_node("agent", agent)

tool_node = ToolNode(tools)
workflow.add_node("tools", tool_node)
workflow.add_edge(START, "agent")
workflow.add_conditional_edges(
    "agent",
    should_continue,
)
workflow.add_edge("tools", "agent")

graph = workflow.compile()

res=graph.invoke(
    input={"messages": [HumanMessage(content="How will the weather be tommorrow?")]}
)

print(res["messages"][-1].content[0]["text"])

result=graph.invoke(input={
    "messages": [HumanMessage(content="Who is the owner and what are the timings?")]
})

print(result["messages"][-1].content[0]["text"])