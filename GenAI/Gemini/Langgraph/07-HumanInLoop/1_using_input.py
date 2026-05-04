from typing import TypedDict, Annotated
from langgraph.graph import add_messages, StateGraph, END
from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage


load_dotenv()

GROQ_API_KEY=os.getenv("GROQ_API_KEY")

os.environ["GROQ_API_KEY"]=GROQ_API_KEY

llm=ChatGroq(model="llama-3.3-70b-versatile")

GENERATE_POST="generate_post"
GET_REVIEW_DECISION="get_review_decision"
POST="post"
COLLECT_FEEDBACK="collect_feedback"

class State(TypedDict):
    messages: Annotated[list, add_messages]

def generate_post(state:State):
    return {
        "messages":[llm.invoke(state["messages"])]
    }

def get_review_decision(state:State):
    post_content=state["messages"][-1].content

    print("\n Current LinkedIn Post:\n")
    print(post_content)
    print("\n")

    decision=input("Post to LinkedIn? (yes/no): ")

    if(decision.lower()=="yes"):
        return POST
    else:
        return COLLECT_FEEDBACK
    
def post(state:State):
    final_post=state["messages"][-1].content
    print("\n Final LinkedIn Post:\n")
    print(final_post)
    print("\n Post has been approved and is now live on LinkedIn")

def collect_feedback(state:State):
    feedback=input("how can i improve this post?")
    return {
        "messages":[HumanMessage(content=feedback)]
    }

graph=StateGraph(State)

graph.add_node(GENERATE_POST, generate_post)
graph.add_node(GET_REVIEW_DECISION,get_review_decision)
graph.add_node(COLLECT_FEEDBACK,collect_feedback)
graph.add_node(POST,post)

graph.set_entry_point(GENERATE_POST)
graph.add_conditional_edges(GENERATE_POST,get_review_decision)
graph.add_edge(POST,END)
graph.add_edge(COLLECT_FEEDBACK, GENERATE_POST)

app=graph.compile()

response=app.invoke({
    "messages": [HumanMessage(
        content="write a LinkedIN post on the topic Agents taking over content creation"
    )]
})

