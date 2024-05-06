from fastapi import HTTPException
from pymongo import errors, DESCENDING
from bson import ObjectId
import random
from datetime import datetime
from app.db import get_db
from app.ml.CollectionGenerator import CollectionGenerator
from app.ml.TechpackGenerator import TechpackGenerator
from app.ml.ItemGenerator import ItemGenerator

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
            collection_name =  CollectionGenerator.generate_collection_description(collection_name)
            return {"description": collection_name}
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
    def generate_collection(collection_data):
        db = get_db()
        try:
            s3_url = CollectionGenerator.generate_collection_image(collection_data['description'])
            collection_data['image_url'] = s3_url
            result = db.collections.insert_one(collection_data)
            collection_data['id'] = str(result.inserted_id)
            return collection_data
        except errors.DuplicateKeyError:
            raise HTTPException(status_code=400, detail="Collection with this title already exists")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to create collection: {str(e)}")

    @staticmethod
    def generate_collection_items_in_background(collection_id):
        db = get_db()
        try:
            collection = db.collections.find_one({"_id": ObjectId(collection_id)})
            if not collection:
                raise HTTPException(status_code=404, detail="Collection not found")
            
            collection_items = CollectionGenerator.generate_full_collection(collection['description'])
            for item in collection_items:
                item['collection'] = ObjectId(collection_id)
                item_image, references = ItemGenerator.generate_item(item['item_description'], gender="female" if item['womanswear'] else "male")
                techpack_url = TechpackGenerator.generate_techpack_url(item_image)
                db.items.insert_one({
                    "title": item['item_name'],
                    "description": item['item_description'],
                    "image_urls": [item_image] + references,
                    "collection": item['collection'],
                    "womanswear": item['womanswear'],
                    "created_at": datetime.now(),
                    "techpack_url": techpack_url
                })
        except Exception as e:
            print(f"Error generating items for collection {collection_id}: {str(e)}")

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
        print()
        collections = list(db.collections.find().sort([("created_at", DESCENDING)]).skip(offset).limit(limit))
        print(collections)
        for collection in collections:
            collection['id'] = str(collection['_id'])
        return collections
    
    @staticmethod
    def check_collection_status(collection_id):
        db = get_db()
        collection = db.collections.find_one({"_id": ObjectId(collection_id)})
        if not collection:
            raise HTTPException(status_code=404, detail="Collection not found")
        
        # Fetch count of items belonging to this collection
        item_count = db.items.count_documents({"collection": ObjectId(collection_id)})
        return {"collection_id": collection_id, "status": "in-progress", "items_processed": item_count}