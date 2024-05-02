from pymongo import MongoClient
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_openai import OpenAIEmbeddings


# create wrapper class for mongo vectorstore
class MongoVectorStore:
    def __init__(self, connection_string, db, collection, vector_search_index):
        self.client = MongoClient(connection_string)
        self.connection_string = connection_string
        self.db_name = db
        self.collection = collection
        self.vector_search_index = vector_search_index

    def initialize(self):
        return MongoDBAtlasVectorSearch.from_connection_string(
            connection_string=self.connection_string,
            namespace=f"{self.db_name}.{self.collection}",
            embedding=OpenAIEmbeddings(disallowed_special=()),
            index_name=self.vector_search_index,
        )
