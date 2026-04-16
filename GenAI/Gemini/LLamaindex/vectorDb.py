from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.core import Settings
from llama_index.core import StorageContext
import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from llama_index.core.node_parser import SentenceSplitter
from llama_index.vector_stores.pinecone import PineconeVectorStore

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

PINECONE_KEY= os.getenv("PINECONE_KEY")

os.environ["GOOGLE_API_KEY"] = GEMINI_API_KEY
os.environ["PINECONE_API_KEY"] = PINECONE_KEY

embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001",
 output_dimensionality=768
)

# #connect to Pinecone index
# PineconeVectorStore: This tells LlamaIndex that your "filing cabinet" is Pinecone. Instead of keeping data in your computer's RAM, it will send everything to Pinecone's cloud servers.
index_name="rag-index"
vectorstore=PineconeVectorStore(index_name=index_name)

llm=GoogleGenAI(model="gemini-3-flash-preview")

Settings.llm=llm
Settings.embed_model=embeddings
Settings.node_parser=SentenceSplitter(chunk_size=512, chunk_overlap=20)


# Set up the storage context
def upload():
    # StorageContext: This acts as a container that carries your storage configuration. It tells the index, "Whenever you save or look for data, use that Pinecone vectorstore."
    storage_context = StorageContext.from_defaults(vector_store=vectorstore)

    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, "data")

    documents = SimpleDirectoryReader(data_path).load_data()

    # This is the "heavy lifting" line. It does three things:

    # Takes your documents and splits them into chunks.

    # Turns those chunks into embeddings (vectors).

    # Uploads those vectors and the original text to Pinecone
    VectorStoreIndex.from_documents(documents, storage_context=storage_context, embed_model=embeddings)

def query(q:str):
    index = VectorStoreIndex.from_vector_store(vectorstore)
    query_engine=index.as_query_engine()
    response=query_engine.query(q)
    print(response)

#upload()
query("What is the timing for exam")
