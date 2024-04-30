from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Create a global variable for the database client
db_client = None

def global_init():
    load_dotenv()  # Ensure environment variables are loaded
    mongodb_uri = os.getenv("MONGO_URI")
    if not mongodb_uri:
        raise Exception("MONGO_URI not found in environment variables")

    global db_client
    print(f"Connecting to MongoDB at {mongodb_uri}")
    db_client = MongoClient(mongodb_uri)

def get_db():
    if not db_client:
        raise Exception("Database not initialized. Call global_init first.")
    return db_client["test"]  # Adjust the database name as needed
