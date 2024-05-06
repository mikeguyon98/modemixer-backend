from fastapi import HTTPException
from pymongo import errors
from bson import ObjectId
from app.db import get_db
from app.ml.ItemGenerator import ItemGenerator
from app.ml.TechpackGenerator import TechpackGenerator
from app.ml.utils.markdown_to_pdf import upload_pdf_to_s3

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
    def generate_item(item_data):
        db = get_db()
        gender = "female" if item_data["womanswear"] else "male"
        try:
            image_url, references = ItemGenerator.generate_item(item_data['description'], gender)
            item_data["image_urls"] = [image_url] + references
            result = db.items.insert_one(item_data)
            item_data['id'] = str(result.inserted_id)
            return item_data
        except errors.DuplicateKeyError:
            raise HTTPException(status_code=400, detail="Item with this title already exists")
    
    @staticmethod
    def regenerate_item(item_data):
        db = get_db()
        item = db.items.find_one({"_id": ObjectId(item_data['id'])})
        print(item)
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        gender = "female" if item_data["womanswear"] else "male"
        new_image_url, references = ItemGenerator.generate_item(item_data['description'], gender)
        item_data["image_urls"] = [new_image_url] + references
        item["image_urls"] = item_data["image_urls"]
        item["description"] = item_data["description"]
        item["title"] = item_data["title"]
        item["womanswear"] = item_data["womanswear"]
        item["techpack_url"] = ""
        item["created_at"] = item_data["created_at"]
        db.items.update_one({"_id": ObjectId(item_data['id'])}, {"$set": item})
        item['id'] = str(item['_id'])
        item["_id"] = str(item["_id"])
        item['collection'] = str(item['collection'])
        return item
            
    @staticmethod
    def read_item_by_id(item_id):
        db = get_db()
        item = db.items.find_one({"_id": ObjectId(item_id)})
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        item['id'] = str(item['_id'])
        item["_id"] = str(item["_id"])
        item['collection'] = str(item['collection'])
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
    
    @staticmethod
    def delete_item(item_id):
        db = get_db()
        result = db.items.delete_one({"_id": ObjectId(item_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Item not found")
        return {"message": "Item deleted successfully"}
    
    @staticmethod
    def update_item(item_data):
        db = get_db()
        item = db.items.find_one({"_id": ObjectId(item_data['id'])})
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        db.items.update_one({"_id": ObjectId(item_data['id'])}, {"$set": item_data})
        return item_data
    
    @staticmethod
    def generate_techpack(item_data):
        db = get_db()
        item = db.items.find_one({"_id": ObjectId(item_data['id'])})
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        try:
            if len(item['image_urls']) == 0:
                raise HTTPException(status_code=400, detail="Item does not have an image")
            pdf_url = TechpackGenerator.generate_techpack_url(item['image_urls'][0])
            # Update the database with the new tech pack URL
            updated_item = db.items.update_one(
                {"_id": ObjectId(item_data['id'])},
                {"$set": {"techpack_url": pdf_url}}
            )
            # Return the updated item data with the tech pack URL
            updated_item_data = db.items.find_one({"_id": ObjectId(item_data['id'])})
            if updated_item_data:
                updated_item_data["id"] = str(updated_item_data["_id"])
                updated_item_data["_id"] = str(updated_item_data["_id"])
                updated_item_data["collection"] = str(updated_item_data["collection"])
                return updated_item_data
            else:
                raise HTTPException(status_code=500, detail="Failed to fetch updated item data")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to generate tech pack: {e}")
        
    @staticmethod
    def generate_description(collection_id, item_name, item_womanswear):
        db = get_db()
        collection = db.collections.find_one({"_id": ObjectId(collection_id)})
        gender = "womanswear" if item_womanswear else "menswear"
        if not collection:
            raise HTTPException(status_code=404, detail="Collection not found")
        try:
            item_description = ItemGenerator.item_description_chain(item_name, gender, collection["description"])
            return {"description": item_description}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to generate item description: {e}")
        