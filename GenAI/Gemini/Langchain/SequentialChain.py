import os
from dotenv import load_dotenv
# from google import genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser 
from langchain_core.runnables import RunnablePassthrough

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
os.environ['GEMINI_API_KEY']=GEMINI_API_KEY

model=ChatGoogleGenerativeAI(
    model="gemini-3-flash-preview",
    max_retries=6
)

prompt_template_name=PromptTemplate(
    input_variables=["cuisine"],
    template="I want to open a restaurant for {cuisine} food. Suugest me a fancy name for this. Only give 1 name without any description."
)

chain1=prompt_template_name | model | StrOutputParser()

prompt_template_items=PromptTemplate(
    input_variables=["name"],
    template="Suggest 5 menu items for {name}. Only give me the item names without any description."
)

chain2=prompt_template_items | model | StrOutputParser()

#this will give output of only chain 2
# full_chain={"name":chain1} | chain2

#this will give output of both chains
full_chain={"name":chain1} | RunnablePassthrough.assign(menu=chain2)

response=full_chain.invoke({"cuisine": "Indian"})

print(response)