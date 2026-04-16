from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.core import Settings
from llama_index.core import StorageContext, load_index_from_storage
import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from llama_index.core.node_parser import SentenceSplitter

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

os.environ["GOOGLE_API_KEY"] = GEMINI_API_KEY

current_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(current_dir, "data")

documents = SimpleDirectoryReader(data_path).load_data()

llm=GoogleGenAI(model="gemini-3-flash-preview")

embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001",
 output_dimensionality=768
)

Settings.llm=llm
Settings.embed_model=embeddings
Settings.node_parser=SentenceSplitter(chunk_size=512, chunk_overlap=20)

#This builds the search engine 
index=VectorStoreIndex.from_documents(documents, embed_model=embeddings)

#storing and loading index. vectorstoreindex are stored in ram so to store it in hard drive we use this
index.storage_context.persist()

#this is for loading the index from storage
# storage_context=StorageContext.from_defaults(persist_dir="./storage")

# index=load_index_from_storage(storage_context=storage_context)

query_engine=index.as_query_engine()

response=query_engine.query("What is the examination center")

print(response)