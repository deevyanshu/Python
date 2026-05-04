import os
from dotenv import load_dotenv
# from google import genai
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel
from typing import Literal

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

os.environ['GEMINI_API_KEY']=GEMINI_API_KEY

model=ChatGoogleGenerativeAI(
    model="gemini-3-flash-preview",
    max_retries=6
)

class Feedback(BaseModel):
    sentiment: Literal["positive", "negative", "neutral"]
    summary:str

structured_model=model.with_structured_output(schema=Feedback.model_json_schema(), method="json-schema")

response=structured_model.invoke("I love using Gemini for my projects!")
print(response)