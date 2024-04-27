from pymongo import MongoClient
import os

# Connection URI
client = MongoClient(os.getenv("MONGO_URI"))
# Database name
db = client["test"]