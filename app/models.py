# app/models.py
from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional

class CollectionModel(BaseModel):
    name: str
    description: str = None
    image_url: str = None
    created_at: datetime = datetime.now()
    id: Optional[str] = None

class CollectionReference(BaseModel):
    name: str
    description: str = None
    image_url: str = None
    created_at: datetime = datetime.now()
    id: str = None

class CollectionResponse(BaseModel):
    total_collections: int
    collections: List[CollectionModel]

class CollectionsItems(BaseModel):
    collection_id: str
    item_name: str
    item_description: str = None

class CollectionDescription(BaseModel):
    description: str

class CollectionName(BaseModel):
    name: str

class ItemModel(BaseModel):
    title: str
    description: str = None
    collection: str = None
    womanswear: bool = True
    image_urls: List[str] = []
    collection: str = None
    created_at: datetime = datetime.now()
    techpack_url: Optional[str] = None
    id: Optional[str] = None

class ItemDescription(BaseModel):
    description: str

class ItemReference(BaseModel):
    title: str
    description: str = None
    collection: str = None
    womanswear: bool = True
    image_urls: List[str] = []
    collection: str = None
    created_at: datetime = datetime.now()
    techpack_url: Optional[str] = None
    id: str = None

class FashionReferences(BaseModel):
    image_url: str
    created_at: datetime = datetime.now()
    gender: str = None