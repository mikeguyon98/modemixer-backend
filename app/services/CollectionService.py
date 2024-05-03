from fastapi import HTTPException
from pymongo import errors
from bson import ObjectId
from app.db import get_db
from ml.CollectionGenerator import CollectionGenerator

class CollectionService:
    @staticmethod
    def create_collection(collection_data):
        db = get_db()
        try:
            result = db.collections.insert_one(collection_data)
            collection_data['id'] = str(result.inserted_id)
            return collection_data
        except errors.DuplicateKeyError:
            raise HTTPException(status_code=400, detail="Collection with this title already exists")
        
    @staticmethod
    def generate_collection_items(description):
        try:
            return CollectionGenerator.generate_collection_items(description)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to generate collection items: {str(e)}")
    
    @staticmethod
    def generate_collection_description(collection_name):
        try:
            return CollectionGenerator.generate_collection_description(collection_name)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to generate collection description: {str(e)}")

    @staticmethod
    def read_collection_by_id(collection_id):
        db = get_db()
        collection = db.collections.find_one({"_id": ObjectId(collection_id)})
        if not collection:
            raise HTTPException(status_code=404, detail="Collection not found")
        collection['id'] = str(collection['_id'])
        return collection

    @staticmethod
    def read_all_collections():
        db = get_db()
        print(db)
        collections = list(db.collections.find())
        print(collections)
        for collection in collections:
            collection['id'] = str(collection['_id'])
        return collections
