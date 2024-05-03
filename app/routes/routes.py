from fastapi import APIRouter, Query
from typing import List, Union
from app.models import ItemModel, CollectionModel, ItemReference
from app.services.ItemService import ItemService
from app.services.CollectionService import CollectionService

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
    
@router.post("/collections", response_model=CollectionModel)
async def create_collection(collection: CollectionModel):
    collection_dict = collection.model_dump()
    return CollectionService.create_collection(collection_dict)

@router.get("/collections", response_model=Union[List[CollectionModel], CollectionModel])
async def read_collection(collection_id: str = Query(None, alias="collection_id")):
    if collection_id:
        return CollectionService.read_collection_by_id(collection_id)
    else:
        return CollectionService.read_all_collections()
    