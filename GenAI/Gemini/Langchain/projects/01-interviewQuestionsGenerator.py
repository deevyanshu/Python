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

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

PINECONE_KEY= os.getenv("PINECONE_KEY")

os.environ["PINECONE_API_KEY"] = PINECONE_KEY

os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY

embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001",
 output_dimensionality=768
)

index_name="rag-index"
vectorstore=PineconeVectorStore(index_name=index_name, embedding=embeddings)

loader=PyPDFLoader(r"C:\Users\hp\Desktop\SDGs_Booklet_Web_En.pdf")

documents= loader.load()

text_splitter= RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)

# #print(documents)
# text_gen=""
# for doc in documents:
#     text_gen+=doc.page_content

texts=text_splitter.split_documents(documents)

for text in texts:
    text.metadata={"source":"sdg_booklet"}

#print(texts)
    
model=ChatGoogleGenerativeAI(
    model="gemini-3-flash-preview",
    max_retries=6
)

prompt_template="""
You are an expert in creating questions based on coding materials and documentation. Your goal is to prepare a coder or programmer for their exam and coding tests.
You do this by asking questions about the text below:

----------
{text}
----------

create 10 questions that will prepare the coders or programmers for their tests.
Make sure not to lose any important information. Give only questions and no answers

QUESTIONS:
"""

prompt_questions=ChatPromptTemplate.from_template(prompt_template)

summarize_chain=({"text": RunnablePassthrough()} | prompt_questions | model | StrOutputParser())

ques=summarize_chain.invoke(texts)

#print(ques)

vectorstore.add_documents(texts)

ques_list=ques.split("\n")
final_list=[ques for ques in ques_list if ques.strip() != ""]
#print(final_list)

retriever=vectorstore.as_retriever(search_kwargs={"k":3},
filter={"source":"sdg_booklet"}
)

template="""Answer the question based ONLY on the following context:
{context}

Question: {question}
"""

answer_template=ChatPromptTemplate.from_template(template)

answer_chain=({
    "context": retriever,
    "question": RunnablePassthrough()
} | answer_template| model | StrOutputParser())

for q in final_list:
    print("Question: ", q)
    answer=answer_chain.invoke(q)
    print("Answer: ",answer)


