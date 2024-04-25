# app/config.py
from mongoengine import connect
from dotenv import load_dotenv
import os

load_dotenv()

def global_init():
    mongodb_uri = os.getenv("MONGO_URI")
    print(f"Connecting to MongoDB at {mongodb_uri}")
    
    connect(
        host=mongodb_uri,
    )
