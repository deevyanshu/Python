import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from src.prompt import prompt_template, template

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

PINECONE_KEY= os.getenv("PINECONE_KEY")

os.environ["PINECONE_API_KEY"] = PINECONE_KEY

os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY

def file_processing(file_path):
    loader=PyPDFLoader(file_path)
    documents= loader.load()
    text_splitter= RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    texts=text_splitter.split_documents(documents)
    for text in texts:
        text.metadata={"source":"sdg_booklet"}
    return texts

def llm_pipeline(file_path):
    texts=file_processing(file_path)

    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001",
    output_dimensionality=768
    )

    index_name="rag-index"
    vectorstore=PineconeVectorStore(index_name=index_name, embedding=embeddings)

    model=ChatGoogleGenerativeAI(
    model="gemini-3-flash-preview",
    max_retries=6
    )

    prompt_questions=PromptTemplate(
        input_variables=["text"]
        ,template=prompt_template)
    summarize_chain=({"text": RunnablePassthrough()} | prompt_questions | model | StrOutputParser())

    ques=summarize_chain.invoke(texts)

    vectorstore.add_documents(texts)

    ques_list=ques.split("\n")
    final_list=[ques for ques in ques_list if ques.strip() != ""]

    retriever=vectorstore.as_retriever(search_kwargs={"k":3},
    filter={"source":"sdg_booklet"}
    )

    answer_template=PromptTemplate(template=template, input_variables=["context","question"])

    answer_chain=({
        "context": retriever,
        "question": RunnablePassthrough()
    } | answer_template| model | StrOutputParser())

    return answer_chain, final_list

