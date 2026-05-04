from git import Repo
import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_text_splitters import Language
from langchain_community.document_loaders.parsers import LanguageParser
from langchain_community.document_loaders.generic import GenericLoader
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.messages import AIMessage

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

PINECONE_KEY= os.getenv("PINECONE_KEY")

os.environ["PINECONE_API_KEY"] = PINECONE_KEY

os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY

embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001", output_dimensionality=768)

index_name="rag-index"
vectorstore=PineconeVectorStore(index_name=index_name, embedding=embeddings)

def upload():
    repo_path="C:\\Users\\hp\\Desktop\\python\\GenAI\\Gemini\\Langchain\\projects\\03-code_analysis\\test_path"

    Repo.clone_from("https://github.com/deevyanshu/URL-SHORTNER.git", to_path=repo_path)

    loader=GenericLoader.from_filesystem(repo_path, glob="**/*.java", parser=LanguageParser(Language.JAVA, parser_threshold=500))

    documents=loader.load()

    #print(documents)

    #this will perform context aware splitting based on the structure of the code (classes, methods, etc.) and not just arbitrary character counts. It will try to keep related code together while splitting.
    documents_splitter=RecursiveCharacterTextSplitter.from_language(language=Language.JAVA,chunk_size=500, chunk_overlap=20)

    texts=documents_splitter.split_documents(documents)

    vectorstore.add_documents(texts)

model=ChatGoogleGenerativeAI(
    model="gemini-3-flash-preview",
    max_retries=6
)

retriever=vectorstore.as_retriever(search_kwargs={"k":3})

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
response=rag_chain.invoke("how authentication works")
print(response)