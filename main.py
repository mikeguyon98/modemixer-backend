import os, pymongo, pprint
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pymongo import MongoClient
from ml.mongo_vectorstore import MongoVectorStore
from ml.generate_trend_vectors import summaries_by_gender
from dotenv import load_dotenv
from app.db import global_init



load_dotenv(dotenv_path="../.env")
global_init()

ATLAS_CONNECTION_STRING = os.getenv("MONGO_URI")

# Connect to your Atlas cluster
client = MongoClient(ATLAS_CONNECTION_STRING)
# Define collection and index name
db_name = "langchain_dn"
collection_name = "trend-men"
atlas_collection = client[db_name][collection_name]
vector_search_index = "vector_index"

# generate the docs
docs_men = summaries_by_gender("male")

# Print the first document
print(docs_men[0])

# Create the vector store
vector_search = MongoDBAtlasVectorSearch.from_documents(
    documents = docs_men,
    embedding = OpenAIEmbeddings(disallowed_special=()),
    collection = atlas_collection,
    index_name = vector_search_index
)

# vector_search = MongoDBAtlasVectorSearch.from_connection_string(
#     connection_string=ATLAS_CONNECTION_STRING,
#     namespace="test.vector",
#     embedding=OpenAIEmbeddings(disallowed_special=()),
#     index_name=vector_search_index
# )



# vector_search = MongoVectorStore(ATLAS_CONNECTION_STRING, db_name, collection_name, vector_search_index).initialize()

query = "MongoDB Atlas security"
results = vector_search.similarity_search(query)
pprint.pprint(results)
