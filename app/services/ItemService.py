from fastapi import HTTPException
from pymongo import errors
from bson import ObjectId
from app.db import db

class ItemService:
    @staticmethod
    def create_item(item_data):
        try:
            result = db.items.insert_one(item_data)
            item_data['id'] = str(result.inserted_id)
            return item_data
        except errors.DuplicateKeyError:
            raise HTTPException(status_code=400, detail="Item with this title already exists")

    @staticmethod
    def read_item_by_id(item_id):
        item = db.items.find_one({"_id": ObjectId(item_id)})
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        item['id'] = str(item['_id'])
        return item

    @staticmethod
    def read_items_by_collection(collection_id):
        items = list(db.items.find({"collection": ObjectId(collection_id)}))
        for item in items:
            item['id'] = str(item['_id'])
            item['collection'] = str(item['collection'])
        return items

    @staticmethod
    def read_all_items():
        items = list(db.items.find())
        for item in items:
            item['id'] = str(item['_id'])
            item['collection'] = str(item['collection'])
        return items