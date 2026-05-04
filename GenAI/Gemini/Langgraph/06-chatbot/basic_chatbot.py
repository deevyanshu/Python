from typing import TypedDict, Annotated
from langgraph.graph import add_messages, StateGraph, END
from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq
from langchain_core.messages import AIMessage, HumanMessage

load_dotenv()

GROQ_API_KEY=os.getenv("GROQ_API_KEY")

os.environ["GROQ_API_KEY"]=GROQ_API_KEY

llm=ChatGroq(model="llama-3.1-8b-instant")

class BasicChatState(TypedDict):
    messages: Annotated[list, add_messages]

def chatbot(state:BasicChatState):
    return {
        "messages": [llm.invoke(state["messages"])]
    }

graph=StateGraph(BasicChatState)

graph.add_node("chatbot",chatbot)
graph.set_entry_point("chatbot")
graph.add_edge("chatbot",END)

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
