#call dalle
from openai import OpenAI
from openai import APIError, RateLimitError, OpenAIError
from fastapi import HTTPException
from .utils.mongo_vectorstore import MongoVectorStore
from .utils.prompt_function import create_prompt
from .utils.webscaper import process_and_upload_image
import os
client = OpenAI()

class ItemGenerator:
    @staticmethod
    def generate_item_image(prompt: str, client: OpenAI = OpenAI()) -> str:
        if len(prompt) > 3900:
            start = len(prompt) - 3900
            prompt = prompt[start:]
        print("PROMPT END:")
        print(prompt[len(prompt) - 500:])
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


    @staticmethod
    def get_context(query: str, gender: str, k: int = 2) -> tuple[str, list[str]]:
        atlas_connection_string = os.getenv("MONGO_URI")
        vector_search_index = "vector_index"
        vector_search_woman = MongoVectorStore(atlas_connection_string, "langchain_db", "FemaleTrend", vector_search_index).initialize()
        vector_search_men = MongoVectorStore(atlas_connection_string, "langchain_db", "MaleTrend", vector_search_index).initialize()

        if gender == "female":
            results = vector_search_woman.similarity_search(query, k=k)
        else:
            results = vector_search_men.similarity_search(query, k=k)
        references = [result.metadata["source"] for result in results]
        context = ""
        for result in results:
            context += result.page_content + " "
        return (context, references)
    
    @staticmethod
    def get_prompt(query: str, gender: str, k: int = 2) -> tuple[str, list[str]]:
        atlas_connection_string = os.getenv("MONGO_URI")
        vector_search_index = "vector_index"
        vector_search_woman = MongoVectorStore(atlas_connection_string, "langchain_db", "FemaleTrend", vector_search_index).initialize()
        vector_search_men = MongoVectorStore(atlas_connection_string, "langchain_db", "MaleTrend", vector_search_index).initialize()

        if gender == "female":
            results = vector_search_woman.similarity_search(query, k=k)
        else:
            results = vector_search_men.similarity_search(query, k=k)
        references = [result.metadata["source"] for result in results]
        context = ""
        for result in results:
            context += result.page_content + " "
        prompt = create_prompt(context, query)
        return (prompt, references)
    

    @staticmethod
    def generate_item(query: str, gender: str, k: int = 2) -> tuple[str, list[str]]:
        prompt, references = ItemGenerator.get_prompt(query, gender, k=k)
        image_url = ItemGenerator.generate_item_image(prompt)
        return (image_url, references)
    
    @staticmethod
    def generate_item_description(item_name: str, gender) -> str:
        context, references = ItemGenerator.get_context(item_name, gender, k=2)
        