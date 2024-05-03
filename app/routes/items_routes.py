from fastapi import APIRouter, Query
from typing import List, Union
from app.models import ItemModel, ItemReference
from app.services.ItemService import ItemService

router = APIRouter()

@router.post("/items", response_model=ItemModel)
async def create_item(item: ItemModel):
    item_dict = item.model_dump()
    return ItemService.create_item(item_dict)

@router.post("/items/generate", response_model=ItemModel)
async def generate_item(item: ItemModel):
    item_dict = item.model_dump()
    return ItemService.generate_item(item_dict)

@router.put("/items/generate", response_model=ItemModel)
async def regenerate_item(item: ItemReference):
    item_dict = item.model_dump()
    return ItemService.regenerate_item(item_dict)

@router.get("/items", response_model=Union[List[ItemModel], ItemModel])
async def read_item(item_id: str = Query(None, alias="item_id"), collection_id: str = Query(None, alias="collection_id")):
    if item_id:
        return ItemService.read_item_by_id(item_id)
    elif collection_id:
        return ItemService.read_items_by_collection(collection_id)
    else:
        return ItemService.read_all_items()
    
@router.delete("/items", response_model=dict)
async def delete_item(item_id: str):
    return ItemService.delete_item(item_id)

@router.put("/items", response_model=ItemModel)
async def update_item(item: ItemReference):
    item_dict = item.model_dump()
    return ItemService.update_item(item_dict)