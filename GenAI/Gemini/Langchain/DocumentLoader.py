import os
from dotenv import load_dotenv
# from google import genai
from langchain_community.document_loaders import TextLoader

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

os.environ["GOOGLE_API_KEY"] = GEMINI_API_KEY

loader=TextLoader("example.txt")
documents= loader.load()

