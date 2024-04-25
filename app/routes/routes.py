from fastapi import APIRouter, HTTPException
from app.models import Item, Collection
from mongoengine.errors import NotUniqueError, ValidationError
from pydantic import BaseModel

router = APIRouter()

class ItemModel(BaseModel):
    title: str
    description: str = None
    price: float
    in_stock: bool = True
    collection: str = None

class CollectionModel(BaseModel):
    name: str
    description: str = None

@router.post("/items/", response_model=ItemModel)
async def create_item(item: ItemModel):
    try:
        item_obj = Item(**item.dict()).save()
        return item_obj
    except NotUniqueError:
        raise HTTPException(status_code=400, detail="Item with this title already exists")
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/items/", response_model=list[ItemModel])
async def read_items():
    items = Item.objects()
    return items

@router.get("/items/{item_id}")
async def read_item(item_id: str):
    item = Item.objects(id=item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.get("/items/collection/{collection_id}")
async def read_items_by_collection(collection_id: str):
    items = Item.objects(collection=collection_id)
    return items

@router.post("/collections/", response_model=CollectionModel)
async def create_collection(collection: CollectionModel):
    try:
        collection_obj = Collection(**collection.dict()).save()
        return collection_obj
    except NotUniqueError:
        raise HTTPException(status_code=400, detail="Collection with this name already exists")
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/collections/", response_model=list[CollectionModel])
async def read_collections():
    collections = Collection.objects()
    return collections

@router.get("/collections/{collection_id}")
async def read_collection(collection_id: str):
    collection = Collection.objects(id=collection_id).first()
    if collection is None:
        raise HTTPException(status_code=404, detail="Collection not found")
    return collection
