import os
from dotenv import load_dotenv
# from google import genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.output_parsers import StrOutputParser 

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

os.environ["GOOGLE_API_KEY"] = GEMINI_API_KEY

model=ChatGoogleGenerativeAI(
    model="gemini-3-flash-preview",
    max_retries=6
)

'''
MessagesPlaceholder(variable_name="chat_history") is the most important part of the prompt.

It creates a dynamic slot in your prompt.

When the code runs, LangChain will take all previous messages from that specific user and "inject" them into this spot.

To Gemini, it looks like one long transcript of a conversation.
'''
prompt=ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{user_input}")
    ]
)

chain=prompt | model | StrOutputParser()

store={}

def get_session_history(session_id):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

'''
"Brain" Wrapper (RunnableWithMessageHistory)
This is the "manager" that connects everything. Instead of you manually saving and loading messages, this wrapper does it for you:

Before the prompt hits Gemini, it calls get_session_history to pull the old chat logs.

After Gemini responds, it automatically saves both your question and Gemini's answer back into the store.
'''
chain_with_memory= RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="user_input",
    history_messages_key="chat_history"
)

config={"configurable":{"session_id":"user_123"}}

response=chain_with_memory.invoke(
    {"user_input": "my name is dev"},
    config=config
)

print(response)

response2=chain_with_memory.invoke(
    {"user_input": "what is my name?"},
    config=config
)

print(response2)
