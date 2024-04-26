# app/models.py
from mongoengine import Document, StringField, DateField
from datetime import datetime

class Collection(Document):
    name = StringField(required=True)
    description = StringField()

class Item(Document):
    title = StringField(required=True)
    description = StringField()
    collection = StringField()  # Reference to Collection if needed
    tech_pack = StringField()

class MensFashionReferences(Document):
    image_url = StringField(required=True)
    date = DateField(default=datetime.now)

class WomansFashionReferences(Document):
    image_url = StringField(required=True)
    date = DateField(default=datetime.now)