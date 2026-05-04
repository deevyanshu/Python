from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


generation_prompt= ChatPromptTemplate.from_messages([
    (
        "system",
        "you are a twitter techie influencer assistant tasked with writing excellent twitter posts."
        "Generate the best twitter post possible for the user's request."
        "If the user provides critique, respond with a revised version of your previous attempts."
    ),
    MessagesPlaceholder(variable_name="messages")
])

reflection_prompt=ChatPromptTemplate.from_messages(
    [
    (
        "system",
        "you are a viral twitter influencer grading a tweet. Generate critique and recommendations for the user's tweet."
        "Always provide detailed recommendations, including requests for length, virality, style, etc."
    ),
    MessagesPlaceholder(variable_name="messages")
])

llm= ChatGoogleGenerativeAI(model="gemini-3-flash-preview",
    max_retries=6
)

generation_chain=generation_prompt | llm

reflection_chain= reflection_prompt | llm