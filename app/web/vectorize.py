# https://python.langchain.com/docs/modules/data_connection/vectorstores/integrations/mongodb_atlas

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders import WebBaseLoader
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import MongoDBAtlasVectorSearch
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

# Step 1: Load
loaders = [
    WebBaseLoader("https://en.wikipedia.org/wiki/AT%26T"),
    WebBaseLoader("https://en.wikipedia.org/wiki/Bank_of_America"),
]
data = []
for loader in loaders:
    data.extend(loader.load())

# Step 2: Transform (Split)
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=0,
    separators=["\n\n", "\n", "(?<=\. )", " "],
    length_function=len,
)
docs = text_splitter.split_documents(data)
print("Split into " + str(len(docs)) + " docs")

# Step 3: Embed
# https://api.python.langchain.com/en/latest/embeddings/langchain.embeddings.openai.OpenAIEmbeddings.html
embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))

# Step 4: Store
# Initialize MongoDB python client
client = MongoClient(os.getenv("MONGO_URI"))
collection = client["test"]["FashionReference"]

# Reset w/out deleting the Search Index
collection.delete_many({})

# Insert the documents in MongoDB Atlas with their embedding
# https://github.com/hwchase17/langchain/blob/master/langchain/vectorstores/mongodb_atlas.py
docsearch = MongoDBAtlasVectorSearch.from_documents(
    docs, embeddings, collection=collection, index_name="vsearch_index"
)
