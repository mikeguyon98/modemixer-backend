from fastapi import APIRouter, Query
from typing import List, Union
from app.models import CollectionModel, CollectionReference, CollectionName, CollectionsItems, CollectionDescription
from app.services.CollectionService import CollectionService

router = APIRouter()
@router.post("/collections", response_model=CollectionModel)
async def create_collection(collection: CollectionModel):
    collection_dict = collection.model_dump()
    return CollectionService.create_collection(collection_dict)

@router.delete("/collections", response_model=dict)
async def delete_collection(collection_id: str):
    return CollectionService.delete_collection(collection_id)

@router.put("/collections", response_model=CollectionModel)
async def update_collection(collection: CollectionReference):
    collection_dict = collection.model_dump()
    return CollectionService.update_collection(collection_dict)

@router.post("/collections/generate_image", response_model=dict)
async def generate_collection_image(collection: CollectionName):
    collection_dict = collection.model_dump()
    return CollectionService.generate_collection_image(collection_dict.get("name"))

@router.post("/collections/generate_items", response_model=List[CollectionsItems])
async def generate_collection_items(collection: CollectionModel):
    collection_dict = collection.model_dump()
    return CollectionService.generate_collection_items(collection_dict.get("description"))

@router.post("/collections/generate_collection_description", response_model=CollectionDescription)
async def generate_collection_description(collection: CollectionName):
    collection_dict = collection.model_dump()
    return CollectionService.generate_collection_description(collection_dict.get("name"))

@router.get("/collections", response_model=Union[List[CollectionModel], CollectionModel])
async def read_collection(collection_id: str = Query(None, alias="collection_id")):
    if collection_id:
        return CollectionService.read_collection_by_id(collection_id)
    else:
        return CollectionService.read_all_collections()