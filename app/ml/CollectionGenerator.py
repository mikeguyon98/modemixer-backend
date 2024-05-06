from openai import OpenAI
from openai import APIError, RateLimitError, OpenAIError
from fastapi import HTTPException
import os
import random
from .utils.dbrx_model import call_dbrx, call_gpt_4_turbo
from .utils.webscaper import process_and_upload_image
from .ItemGenerator import ItemGenerator


class CollectionGenerator:
    @staticmethod
    def get_dbrx_client():
        """ Initialize the OpenAI client with a Databricks token. """
        DATABRICKS_TOKEN = os.getenv('DATABRICKS_TOKEN')
        client = OpenAI(
            api_key=DATABRICKS_TOKEN,
            base_url="https://dbc-47b29bb9-5648.cloud.databricks.com/serving-endpoints"
        )
        return client

    @staticmethod
    def generate_collection_items(collection_description: str):
        """ Generate a list of items for a given collection name. """
        messages=[
            {
                "role": "system",
                "content": ("You are a fashion designer and you are assigned with the task of "
                            "designing a new collection for the upcoming season. The input will be the "
                            "collection description and the output should be a comma-separated list of the names "
                            "of 5 items in the collection. ONLY OUTPUT THE COMMA SEPARATED LIST NOTHING ELSE! "
                            "EXAMPLE: \n COLLECTION DESCRIPTION: Embrace the glamour and warmth of a" 
                            "luxurious winter retreat with 'Aspen Elegance: Winter Luxe.' This collection" 
                            "features sumptuous fabrics and sophisticated designs, perfect for snowy days and"
                            "cozy nights. Each piece combines timeless elegance with modern comfort, ensuring"
                            "you look effortlessly chic whether on the slopes or by the fireside. \n OUTPUT:"
                            " \n "
                            "Snowfall Serenity Coat, Alpine Whisper Sweater, Frostbound Velvet Dress, "
                            "Glacial Glamour Boots, Evergreen Embrace Scarf")
            },
            {
                "role": "user",
                "content": f"COLLECTION DESCRIPTION: {collection_description}"
            }
        ]
        result = call_gpt_4_turbo(messages)
        return result.split(", ")
    
    @staticmethod
    def generate_collection_description(collection_name: str, brand_identity: str = None):
        """ Generate a description for a collection based on its name. """
        system_message = {
            "role": "system",
            "content": ("You are a fashion designer and you are assigned with the task of designing a new "
                        "collection for the upcoming season. The input will be the collection name and the  "
                        "output will be an collection description. Here is some information about your brand "
                        "identity that you can use as inspiration (if blank ignore): \n\n" + (brand_identity if brand_identity else "") + "\n\n"
                        "ONLY RESPOND WITH THE COLLECTION DESCRIPTION NOTHING ELSE! "
                        "EXAMPLE: \n COLLECTION NAME: Aspen Elegance: Winter Luxe \n OUTPUT: \n"
                        "Embrace the glamour and warmth of a" 
                        "luxurious winter retreat with Aspen Elegance: Winter Luxe. This collection" 
                        "features sumptuous fabrics and sophisticated designs, perfect for snowy days and"
                        "cozy nights. Each piece combines timeless elegance with modern comfort, ensuring"
                        "you look effortlessly chic whether on the slopes or by the fireside."
                        )
            }
        user_message = {
            "role": "user",
            "content": f"COLLECTION NAME: {collection_name}"
        }
        messages = [system_message, user_message]
        return call_dbrx(messages)

    @staticmethod
    def item_description_chain(item_name: str, gender: str):
        """ Generate a description for an item based on its name and gender. """
        context, references = ItemGenerator.get_context(item_name, gender, k=2)
        system_message = {
            "role": "system",
            "content": ("You are a fashion designer and you are assigned with the task of designing a new "
                        "collection for the upcoming season. The input will be the item name and the output "
                        "will be an item description. Here are details of celebrity outfits that you can use "
                        "as inspiration: \n\n" + context + "\n\n"
                        "ONLY RESPOND WITH THE ITEM DESCRIPTION NOTHING ELSE! "
                        "EXAMPLE: \n ITEM NAME: Snowfall Serenity Coat \n OUTPUT: \n Seaside Sophistication Maxi Dress "
                        "Navy and sky blue silk-linen dress with beige lace hem. Features adjustable straps, v-neck, "
                        "and silver waist ribbon. Perfect for elegant summer evenings.")
        }
        user_message = {
            "role": "user",
            "content": f"ITEM NAME: {item_name}"
        }
        messages = [system_message, user_message]
        return call_dbrx(messages)

    @staticmethod
    def generate_full_collection(collection_description: str):
        """ Generate descriptions for each item in a collection. """
        items = CollectionGenerator.generate_collection_items(collection_description)
        return_arr = []
        for item_name in items:
            gender_options = ["male", "female"]
            gender = random.choice(gender_options)
            item_desc = ItemGenerator.item_description_chain(item_name, gender, collection_description)
            return_arr.append({
                "item_name": item_name,
                "item_description": item_desc,
                "womanswear": True if gender == "female" else False
            })
        return return_arr
    
    @staticmethod
    def generate_collection_image(collection_description: str, client: OpenAI = OpenAI()):
        ''' Generate an image for a collection based on its description. '''
        prompt = f"""CONTEXT:
        You are a fashion designer and you are assigned with the task of designing a new collection for the upcoming season. The following is a description of the collection: \n {collection_description} \n\n. You are tasked with designing a cover image for this collection. Keep the image simple, elegant, and visually appealing. The image should capture the essence of the collection and entice customers to explore further. The image should be in a portrait orientation and should be suitable for use on a website or social media platform. \n\n DIRECTIONS: Design a cover image for the collection based on the description provided. The image should be visually appealing and should reflect the theme and style of the collection. Use a plain background and focus on the key elements of the collection. The image should be high-quality and professional. """
        if len(prompt) > 3900:
            start = len(prompt) - 3900
            prompt = prompt[start:]
        try:
            response = client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1,
            )
            url = response.data[0].url
            return process_and_upload_image(url, "modemixer-images")
        except RateLimitError:
            # Handle rate limiting issue, maybe log it and retry or queue
            raise HTTPException(status_code=429, detail="Request rate limit exceeded")
        except APIError as e:
            # Handle generic API errors
            raise HTTPException(status_code=500, detail=f"OpenAI API error: {str(e)}")
        except OpenAIError as e:
            # Handle other OpenAI-specific errors
            raise HTTPException(status_code=500, detail=f"OpenAI service error: {str(e)}")
        except Exception as e:
            # Handle unexpected errors
            raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

