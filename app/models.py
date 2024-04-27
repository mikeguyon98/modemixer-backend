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

class ItemModel(BaseModel):
    title: str
    description: str = None
    collection: str = None
    image_urls: List[str] = []
    collection: str = None
    created_at: datetime = datetime.now()
    id: Optional[str] = None

class MensFashionReferences(BaseModel):
    image_url: str
    created_at: datetime = datetime.now()

class WomansFashionReferences(BaseModel):
    image_url :str
    created_at: datetime = datetime.now()