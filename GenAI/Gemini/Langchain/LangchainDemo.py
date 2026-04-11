import os
from dotenv import load_dotenv
# from google import genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser 

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
os.environ['GEMINI_API_KEY']=GEMINI_API_KEY

model=ChatGoogleGenerativeAI(
    model="gemini-3-flash-preview",
    temperature=0.7,
    max_retries=6
)

# response = model.invoke("why do parrots have colorful feathers")
# print(response.text)

# messages = [
#     (
#         "system",
#         "You are a helpful assistant that translates English to French. Translate the user sentence.",
#     ),
#     ("human", "I love programming."),
# ]
# ai_msg = model.invoke(messages)
# print(ai_msg.text)

prompt_template_name=PromptTemplate(
    input_variables=["name"],
    template="What is the capital of {name}?"
)

# direct way
# p=prompt_template_name.format(name="France")
# response = model.invoke(p)
# print(response.text)

# using chaining
chain=prompt_template_name | model | StrOutputParser()

response=chain.invoke({"name": "India"})
print(response)
