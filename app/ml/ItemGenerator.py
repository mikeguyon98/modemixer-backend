#call dalle
from openai import OpenAI
from .utils.mongo_vectorstore import MongoVectorStore
from .utils.prompt_function import create_prompt
import os
client = OpenAI()

class ItemGenerator:
    def __init__(self):
        pass


    @staticmethod
    def generate_item_image(prompt: str) -> str:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        return response.data[0].url

    @staticmethod
    def get_context(query: str, gender: str) -> tuple[str, list[str]]:
        atlas_connection_string = os.getenv("MONGO_URI")
        vector_search_index = "vector_index"
        vector_search_woman = MongoVectorStore(atlas_connection_string, "langchain_db", "FemaleTrend", vector_search_index).initialize()
        vector_search_men = MongoVectorStore(atlas_connection_string, "langchain_db", "MaleTrend", vector_search_index).initialize()

        if gender == "female":
            results = vector_search_woman.similarity_search(query, k=2)
        else:
            results = vector_search_men.similarity_search(query, k=2)
        references = [result.metadata["source"] for result in results]
        context = ""
        for result in results:
            context += result.page_content + " "
        prompt = create_prompt(context, query)
        return (prompt, references)

    @staticmethod
    def generate_item(query: str, gender: str) -> tuple[str, list[str]]:
        prompt, references = ItemGenerator.get_context(query, gender)
        image_url = ItemGenerator.generate_item_image(prompt)
        return (image_url, references)
    
    @staticmethod
    def generate_item_description(url: str) -> str:
        return None