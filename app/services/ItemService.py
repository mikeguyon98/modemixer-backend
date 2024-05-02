from fastapi import HTTPException
from pymongo import errors
from bson import ObjectId
from app.db import get_db
from app.ml.ItemGenerator import ItemGenerator

class ItemService:
    @staticmethod
    def create_item(item_data):
        db = get_db()
        try:
            result = db.items.insert_one(item_data)
            item_data['id'] = str(result.inserted_id)
            return item_data
        except errors.DuplicateKeyError:
            raise HTTPException(status_code=400, detail="Item with this title already exists")
        
    @staticmethod
    def generate_new_item(item_data):
        db = get_db()
        try:
            image_url, references = ItemGenerator.generate_item(item_data['description'], "male")
            item_data["image_urls"] = [image_url] + references
            result = db.items.insert_one(item_data)
            item_data['id'] = str(result.inserted_id)
            return item_data
        except errors.DuplicateKeyError:
            raise HTTPException(status_code=400, detail="Item with this title already exists")

    @staticmethod
    def read_item_by_id(item_id):
        db = get_db()
        item = db.items.find_one({"_id": ObjectId(item_id)})
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        item['id'] = str(item['_id'])
        return item

    @staticmethod
    def read_items_by_collection(collection_id):
        db = get_db()
        items = list(db.items.find({"collection": ObjectId(collection_id)}))
        for item in items:
            item['id'] = str(item['_id'])
            item['collection'] = str(item['collection'])
        return items

    @staticmethod
    def read_all_items():
        db = get_db()
        items = list(db.items.find())
        for item in items:
            item['id'] = str(item['_id'])
            item['collection'] = str(item['collection'])
        return items