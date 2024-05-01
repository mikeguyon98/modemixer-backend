import requests
from bs4 import BeautifulSoup
import boto3
from dotenv import load_dotenv
import os
import pymongo
import datetime
from pymongo import MongoClient

load_dotenv()


client = MongoClient(os.getenv("MONGO_URI"))
db = client["test"]


def get_image_urls(keyword, total_images):
    search_url = f"https://www.bing.com/images/search?q={keyword.replace(' ', '+')}"
    response = requests.get(search_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    links = soup.find_all("a", class_="iusc")
    image_urls = []

    for link in links:
        m = eval(link["m"])
        image_url = m["murl"]
        if image_url.startswith("https") and image_url.lower().endswith(".jpg"):
            image_urls.append(image_url)

        if len(image_urls) >= total_images:
            break

    return image_urls


def upload_image_to_s3(image_url, bucket_name):
    session = boto3.Session(
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION"),
    )
    s3 = session.client("s3")

    try:
        response = requests.get(image_url, stream=True)
        file_name = image_url.split("/")[-1]
        s3.upload_fileobj(response.raw, bucket_name, file_name)
        print(f"Successfully uploaded {file_name} to S3 bucket {bucket_name}")
        # Get the public URL for the uploaded image
        public_url = f"https://{bucket_name}.s3.amazonaws.com/{file_name}"
        return public_url
    except Exception as e:
        print(f"Failed to upload {image_url}: {e}")
        return None


def get_male_img():
    keyword = "ryan gosling style 2024"
    total_images = 5
    bucket_name = "modemixer-images"

    image_urls = get_image_urls(keyword, total_images)
    for image_url in image_urls:
        s3_url = upload_image_to_s3(image_url, bucket_name)
        document = {
            "url": s3_url,
            "gender": "male",
            "created_at": datetime.datetime.now(),
        }
        db.FashionReference.insert_one(document)
        print(db)
        if db.FashionReference.find_one(document):
            print("Document inserted successfully")
        else:
            print("Failed to insert document")

    response = requests.get(image_urls[0], stream=True)


def get_female_img():
    keyword = "zendeya street style 2024"
    total_images = 5
    bucket_name = "modemixer-images"

    image_urls = get_image_urls(keyword, total_images)
    for image_url in image_urls:
        s3_url = upload_image_to_s3(image_url, bucket_name)
        document = {
            "url": s3_url,
            "gender": "female",
            "created_at": datetime.datetime.now(),
        }
        db.FashionReference.insert_one(document)

    response = requests.get(image_urls[0], stream=True)
