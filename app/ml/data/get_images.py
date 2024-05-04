from db import get_db
from datetime import datetime


def return_images_links_by_gender() -> dict:
    male_fashion_refs = []
    female_fashion_refs = []
    db = get_db()
    all_references = list(db.FashionReference.find())
    for item in all_references:
        if item["gender"] == "male":
            male_fashion_refs.append(item["url"])
        elif item["gender"] == "female":
            female_fashion_refs.append(item["url"])
    
    return {
        "male": male_fashion_refs,
        "female": female_fashion_refs
    }

def return_images_links_by_gender_and_date(date: datetime) -> dict:
    male_fashion_refs = []
    female_fashion_refs = []
    db = get_db()
    # Convert date if it's not already a datetime object
    if not isinstance(date, datetime):
        date = datetime.strptime(date, '%Y-%m-%d')  # Adjust the format as necessary
    
    # Query to find documents where created_at is after the specified date
    query = {"created_at": {"$gt": date}}
    all_references = list(db.FashionReference.find(query))
    
    for item in all_references:
        if item["gender"] == "male":
            male_fashion_refs.append(item["url"])
        elif item["gender"] == "female":
            female_fashion_refs.append(item["url"])
    
    return {
        "male": male_fashion_refs,
        "female": female_fashion_refs
    }

    
