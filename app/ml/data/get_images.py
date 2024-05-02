from db import get_db

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

    
