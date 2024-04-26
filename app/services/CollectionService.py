from fastapi import HTTPException
from pymongo import errors
from bson import ObjectId
from app.db import db

class CollectionService:
    @staticmethod
    def create_collection(collection_data):
        try:
            result = db.collections.insert_one(collection_data)
            collection_data['id'] = str(result.inserted_id)
            return collection_data
        except errors.DuplicateKeyError:
            raise HTTPException(status_code=400, detail="Collection with this title already exists")

    @staticmethod
    def read_collection_by_id(collection_id):
        collection = db.collections.find_one({"_id": ObjectId(collection_id)})
        if not collection:
            raise HTTPException(status_code=404, detail="Collection not found")
        collection['id'] = str(collection['_id'])
        return collection

    @staticmethod
    def read_all_collections():
        collections = list(db.collections.find())
        for collection in collections:
            collection['id'] = str(collection['_id'])
        return collections
