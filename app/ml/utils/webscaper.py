import requests
from bs4 import BeautifulSoup
import boto3
from dotenv import load_dotenv
import os
import datetime
from pymongo import MongoClient
from PIL import Image
import urllib.parse
import io

client = MongoClient(os.getenv("MONGO_URI"))
db = client["test"]

# Convert any image to JPEG
def convert_to_jpeg(image):
    if image.format != 'JPEG':
        image = image.convert('RGB')
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='JPEG')
    return img_byte_arr

def convert_to_png(image):
    if image.format != 'PNG':
        image = image.convert('RGB')
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    return img_byte_arr

# Resize image if larger than 20MB
def resize_image(image, max_size_mb=20) -> io.BytesIO:
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='JPEG')
    img_byte_arr.seek(0)

    if img_byte_arr.getbuffer().nbytes > max_size_mb * 1024 * 1024:  # Convert MB to bytes
        factor = (max_size_mb * 1024 * 1024 / img_byte_arr.getbuffer().nbytes)**0.5
        new_size = (int(image.size[0] * factor), int(image.size[1] * factor))
        image = image.resize(new_size, Image.ANTIALIAS)
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='JPEG')

    return img_byte_arr

def resize_image_png(image, max_size_mb=20) -> io.BytesIO:
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)

    if img_byte_arr.getbuffer().nbytes > max_size_mb * 1024 * 1024:  # Convert MB to bytes
        factor = (max_size_mb * 1024 * 1024 / img_byte_arr.getbuffer().nbytes)**0.5
        new_size = (int(image.size[0] * factor), int(image.size[1] * factor))
        image = image.resize(new_size, Image.ANTIALIAS)
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')

    return img_byte_arr

def search_images_bing(api_key, term, count=10):
    url = "https://api.bing.microsoft.com/v7.0/images/search"
    headers = {"Ocp-Apim-Subscription-Key": api_key}
    params = {"q": term, "imageType": "photo", "count": count}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()
    image_urls = [img["contentUrl"] for img in search_results["value"]]
    return image_urls


def upload_image_to_s3(img_byte_arr, bucket_name, file_name):
    session = boto3.Session(
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION"),
    )
    s3 = session.client("s3")
    
    try:
        s3.upload_fileobj(io.BytesIO(img_byte_arr.getvalue()), bucket_name, file_name)
        print(f"Successfully uploaded {file_name} to S3 bucket {bucket_name}")
        # Get the public URL for the uploaded image, ensuring the file name is URL-encoded
        encoded_file_name = urllib.parse.quote(file_name)
        public_url = f"https://{bucket_name}.s3.amazonaws.com/{encoded_file_name}"
        print(public_url)
        return public_url
    except Exception as e:
        print(f"Failed to upload {file_name}: {e}")
        return None


def process_and_upload_image(image_url, bucket_name):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
    response = requests.get(image_url, stream=True, headers=headers)
    try:
        response.raise_for_status()
        image = Image.open(response.raw)
        img_byte_arr = convert_to_jpeg(image)
        img_byte_arr = resize_image(Image.open(img_byte_arr))
        file_name = f"{image_url.split('/')[-1].split('.')[0]}.jpg"
        return upload_image_to_s3(img_byte_arr, bucket_name, file_name)
    except Exception as e:
        print(f"Error processing image {image_url}: {e}")
        return None



def get_images(references : dict) -> None:
    for man in references["male"]:
        process_image(man, "male")
    for female in references["female"]:
        process_image(female, "female")
    print("Images uploaded successfully")

def process_image(person: str, gender: str) -> None:
    keyword = f"{person} outfits {datetime.datetime.now().year}"
    total_images = 4
    bucket_name = "modemixer-images"
    image_urls = search_images_bing(os.getenv("BING_SEARCH_API_KEY"), keyword, count=total_images)
    for image_url in image_urls:
        s3_url = process_and_upload_image(image_url, bucket_name)
        if s3_url:
            document = {
                "url": s3_url,
                "gender": gender,
                "created_at": datetime.datetime.now(),
            }
            db.FashionReference.insert_one(document)
            if db.FashionReference.find_one(document):
                print("Document inserted successfully")
            else:
                print("Failed to insert document")
        else:
            print(f"Failed to process image {image_url}")
