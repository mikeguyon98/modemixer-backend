from fastapi import HTTPException
from pymongo import errors
from bson import ObjectId
from app.db import get_db
from app.ml.CollectionGenerator import CollectionGenerator

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
    def update_collection(collection_data):
        db = get_db()
        collection = db.collections.find_one({"_id": ObjectId(collection_data['id'])})
        if not collection:
            raise HTTPException(status_code=404, detail="Collection not found")
        db.collections.update_one({"_id": ObjectId(collection_data['id'])}, {"$set": collection_data})
        return collection_data
        
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
    def delete_collection(collection_id):
        db = get_db()
        result = db.collections.delete_one({"_id": ObjectId(collection_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Collection not found")
        return {"message": "Collection deleted successfully"}
    
    @staticmethod
    def generate_collection_image(description):
        try:
            s3_url = CollectionGenerator.generate_collection_image(description)
            return {"image_url": s3_url}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to generate collection image: {str(e)}")
        
    @staticmethod
    def get_total_collections_count():
        db = get_db()
        return db.collections.count_documents({})
    
    @staticmethod
    def read_all_collections(limit: int = 10, offset: int = 0):
        db = get_db()
        collections = list(db.collections.find().sort([("created_at", -1)]).skip(offset).limit(limit))
        for collection in collections:
            collection['id'] = str(collection['_id'])
        return collections