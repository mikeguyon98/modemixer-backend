import getpass, os, pymongo, pprint
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_openai import ChatOpenAI, OpenAIEmbeddings, OpenAI
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pymongo import MongoClient
from langchain.chains import RetrievalQA
import gradio as gr
from gradio.themes.base import Base
from dotenv import load_dotenv

load_dotenv()

# This code allows you to ask question about the custome knowledge stored in MongoDB

client = MongoClient(os.getenv("MONGO_URI"))
dbName = "langchain_demo"
collectionName = "collection_of_text_blobs"
collection = client[dbName][collectionName]

embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
vectorStore = MongoDBAtlasVectorSearch(collection, embeddings)


def query_data(query):
    retriever = vectorStore.as_retriever(
        search_type="similarity", search_kwargs={"k": 10, "score_threshold": 0.75}
    )
    llm = OpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"), temperature=0)
    qa = RetrievalQA.from_chain_type(llm, chain_type="stuff", retriever=retriever)
    retriever_output = qa.invoke(query)
    return retriever_output


ret_result = query_data("What is yaw?")
print(ret_result)
