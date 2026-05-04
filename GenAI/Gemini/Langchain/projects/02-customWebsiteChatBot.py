import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.document_loaders import UnstructuredURLLoader
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
vectorstore=PineconeVectorStore(index_name=index_name, embedding=embeddings, namespace="default")

URLs=[
    'https://medium.com/@lucnguyen_61589/llama-2-using-huggingface-part-1-3a29fdbaa9ed',
    'https://www.mosaicml.com/blog/mpt-7b'
]

loaders=UnstructuredURLLoader(urls=URLs)

data=loaders.load()

#print(data)

text_splitter= CharacterTextSplitter(separator='\n',chunk_size=1000, chunk_overlap=100)

text_chunks=text_splitter.split_documents(data)

vectorstore.add_documents(text_chunks)

model=ChatGoogleGenerativeAI(
    model="gemini-3-flash-preview",
    max_retries=6
)

retrievar=vectorstore.as_retriever(
    search_kwargs={"k":3}
)

template="""Answer the question based ONLY on the following context:
{context}

Question: {question}
"""

answer_template=ChatPromptTemplate.from_template(template)

chain=({
    "context": retrievar,
    "question": RunnablePassthrough()
} | answer_template| model | StrOutputParser())

response=chain.invoke("What is the MPT-7B model?")

print(response)
