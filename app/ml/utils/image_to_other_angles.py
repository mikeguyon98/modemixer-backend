from openai import OpenAI
from openai.types.chat.chat_completion import Choice
from PIL import Image
import requests
import uuid
from datetime import datetime
from ml.utils.webscaper import  resize_image, convert_to_jpeg, upload_image_to_s3
from io import BytesIO

def generate_other_image_angles(image_url: str, client: OpenAI= OpenAI()) -> str:
    try:
        # Upload image to S3
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
        response = requests.get(image_url, stream=True, headers=headers)
        response.raise_for_status()
        image = Image.open(response.raw)
        img_byte_arr = convert_to_jpeg(image)
        img_byte_arr = resize_image(Image.open(img_byte_arr))
        #generate random file name
        
        file_name = f"{uuid.uuid4()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        s3_url = upload_image_to_s3(img_byte_arr, "modemixer-images", file_name)
        if s3_url:
            description = image_to_description(s3_url, client)
        else:
            raise Exception("Failed to upload image to S3")
        prompt = f"I will provide a description of a clothing item and I want you to create the exact item based on the description. I will evaluate you on how similar your version is to the real item. Create an image of a person modeling the item with a landscape background fitting of the clothing item \n DESCRIPTION: \n {description}"
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
            
    except Exception as e:
        print(f"Error processing image {image_url}: {e}")
        return None
    return response.data[0].url

def image_to_description(img_url: str, client: OpenAI= OpenAI()) -> str:
    response = client.chat.completions.create(
    model="gpt-4-vision-preview",
    messages=[
        {
        "role": "user",
        "content": [
            {"type": "text", "text": "Describe the clothing item in this image in extremely great detail. Fine enough detail that a painter would be able to recreate the exact image from the description alone."},
            {
            "type": "image_url",
            "image_url": {
                "url": f"{img_url}",
            },
            },
        ],
        }
    ],
    max_tokens=300,
    )
    return response.choices[0]