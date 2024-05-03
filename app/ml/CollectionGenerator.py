from openai import OpenAI
import os
from dotenv import load_dotenv
from db import global_init
import random
from .utils.dbrx_model import call_dbrx
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
    def generate_collection_items(collection_name: str):
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
                "content": f"COLLECTION NAME: {collection_name}"
            }
        ]
        result = call_dbrx(messages)
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
    def generate_full_collection(collection_name: str):
        """ Generate descriptions for each item in a collection. """
        items = CollectionGenerator.generate_collection_items(collection_name)
        return_arr = []
        for item_name in items:
            gender_options = ["male", "female"]
            gender = random.choice(gender_options)
            item_desc = CollectionGenerator.item_description_chain(item_name, gender)
            return_arr.append({
                "item_name": item_name,
                "item_description": item_desc
            })
        return return_arr