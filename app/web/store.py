from pymongo import MongoClient
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import MongoDBAtlasVectorSearch
from langchain_community.document_loaders import DirectoryLoader
import os
from dotenv import load_dotenv

load_dotenv()
# Store files in MongoDB Vector Database

client = MongoClient(os.getenv("MONGO_URI"))
dbName = "langchain_demo"
collectionName = "collection_of_text_blobs"
collection = client[dbName][collectionName]
search_index_name = "demo_index"
loader = DirectoryLoader(
    "./web/sample_files",
    glob="./*.txt",
    show_progress=True,
)
data = loader.load()

embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
vectorStore = MongoDBAtlasVectorSearch.from_documents(
    data, embeddings, collection=collection, index_name=search_index_name
)
