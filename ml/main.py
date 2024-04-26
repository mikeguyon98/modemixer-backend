import os, pymongo, pprint
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pymongo import MongoClient
from mongo_vectorstore import MongoVectorStore
from dotenv import load_dotenv

load_dotenv(dotenv_path="../.env")

ATLAS_CONNECTION_STRING = os.getenv("MONGO_URI")

# Connect to your Atlas cluster
client = MongoClient(ATLAS_CONNECTION_STRING)
# Define collection and index name
db_name = "test"
collection_name = "vector"
atlas_collection = client[db_name][collection_name]
vector_search_index = "vector_index"

# Load the PDF
loader = PyPDFLoader("https://query.prod.cms.rt.microsoft.com/cms/api/am/binary/RE4HkJP")
data = loader.load()
# Split PDF into documents
text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=20)
docs = text_splitter.split_documents(data)
# Print the first document
print(docs[0])

# Create the vector store
# vector_search = MongoDBAtlasVectorSearch.from_documents(
#     documents = docs,
#     embedding = OpenAIEmbeddings(disallowed_special=()),
#     collection = atlas_collection,
#     index_name = vector_search_index
# )

# vector_search = MongoDBAtlasVectorSearch.from_connection_string(
#     connection_string=ATLAS_CONNECTION_STRING,
#     namespace="test.vector",
#     embedding=OpenAIEmbeddings(disallowed_special=()),
#     index_name=vector_search_index
# )  

vector_search = MongoVectorStore(ATLAS_CONNECTION_STRING, db_name, collection_name, vector_search_index).initialize()

query = "MongoDB Atlas security"
results = vector_search.similarity_search(query)
pprint.pprint(results)