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

#initialize embeddings
embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001",
 output_dimensionality=768
)

#connect to Pinecone index
index_name="rag-index"
vectorstore=PineconeVectorStore(index_name=index_name, embedding=embeddings)

#load and split 
# loader=PyPDFLoader(r"C:\Users\hp\Desktop\DeevyanshuGarg_Resume (1).pdf")
# documents= loader.load()

# text_splitter= RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
# texts=text_splitter.split_documents(documents)

# #adding metadata to the documents
# for text in texts:
#     text.metadata["source"]= "resume"

# #upload to pineconce
# vectorstore.add_documents(texts)

model=ChatGoogleGenerativeAI(
    model="gemini-3-flash-preview",
    max_retries=6
)

#setup the retriever
retriever=vectorstore.as_retriever(search_kwargs={"k":3},
filter={"source":"resume"}
) #get top 3 results

#define the prompt template
template="""Answer the question based ONLY on the following context:
{context}

Question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)

rag_chain=({
    "context": retriever,
    "question": RunnablePassthrough()}
    | prompt
    | model
    | StrOutputParser()
)

#invoke
response=rag_chain.invoke("What are the skills mentioned in the resume?")
print(response)

