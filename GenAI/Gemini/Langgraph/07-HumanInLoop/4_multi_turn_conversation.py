from typing import TypedDict, Annotated, List
from langgraph.graph import add_messages, StateGraph, END
from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langgraph.types import Command, interrupt
from langgraph.checkpoint.memory import MemorySaver
import uuid

load_dotenv()

GROQ_API_KEY=os.getenv("GROQ_API_KEY")

os.environ["GROQ_API_KEY"]=GROQ_API_KEY

llm=ChatGroq(model="llama-3.3-70b-versatile")

class State(TypedDict):
    linkedIn_topic:str
    generated_post: Annotated[List[str], add_messages]
    human_feedback: Annotated[List[str], add_messages]

def model(state:State):
    """Here, we are using the LLM to generate a LinkedIn post with human feedback incorporated"""
    print("[model] Generating Content")
    linkedIn_topic=state["linkedIn_topic"]
    feedback=state["human_feedback"] if "human_feedback" in state else ["No feedback yet"]

    prompt=f"""
        LinkedIn_topic: {linkedIn_topic}
        Human feedback: {feedback[-1] if feedback else "No feedback yet"}

        Generate a Structured and well-written LinkedIn post based on the given topic.

        Consider previous human feedback to refine the response
    """
    response=llm.invoke([
        SystemMessage(content="You are an expert LinkedIN content writer"),
        HumanMessage(content=prompt)
    ])

    generated_linkedIn_post=response.content

    print(f"[model_node] Generated LinkedIn Post: \n{generated_linkedIn_post}")

    return {"generated_post":[AIMessage(content=generated_linkedIn_post)],
    "human_feedback": feedback
    }

def human_node(state:State):
    """Human intervention node - loops back to model unless input is done"""
    print("\n [human_node] writing human feedback...")

    generated_post=state["generated_post"]

    user_feedback=interrupt(
        {
            "generated_post": generated_post,
            "message":"Provide feedback or type 'done' to finish"
        }
    )

    print(f"[human_node] Received human feedback: {user_feedback}")

    if user_feedback.lower()=="done":
        return Command(update={"human_feedback": state["human_feedback"]+["Finalised"]}, goto="end_node")
    
    return Command(update={"human_feedback": state["human_feedback"]+[user_feedback]}, goto="model")

def end_node(state:State):
    """Final Node """
    print("\n [end_node] Process finished")
    print("Final generated post:", state["generated_post"][-1])
    print("Final human feedback:", state["human_feedback"])
    return {
        "generated_post": state["generated_post"],
        "human_feedback": state["human_feedback"]
    }

graph=StateGraph(State)

graph.add_node("model", model)
graph.add_node("human_node",human_node)
graph.add_node("end_node", end_node)

graph.set_entry_point("model")
graph.add_edge("model","human_node")

graph.set_finish_point("end_node")

checkpointer=MemorySaver()

app=graph.compile(checkpointer=checkpointer)

config={"configurable":
        {
           "thread_id":uuid.uuid4() 
        }}

linkedIn_topic=input("Enter topic: ")
initial_state={
    "linkedIn_topic": linkedIn_topic,
    "generated_post": [],
    "human_feedback": []
}

for chunk in app.stream(initial_state,config=config):
    for node_id, value in chunk.items():
        if(node_id=="__interrupt__"):
            while True:
                user_feedback=input("Provide feedback or type 'done' to finish: ")

                app.invoke(Command(resume=user_feedback),config)

                if user_feedback.lower()=="done":
                    break