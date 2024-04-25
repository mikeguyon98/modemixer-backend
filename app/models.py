# app/models.py
from mongoengine import Document, StringField

class Collection(Document):
    name = StringField(required=True)
    description = StringField()

class Item(Document):
    title = StringField(required=True)
    description = StringField()
    collection = StringField()  # Reference to Collection if needed
    tech_pack = StringField()

