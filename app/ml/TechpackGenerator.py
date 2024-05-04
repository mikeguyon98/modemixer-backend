from typing import List
from openai import OpenAI

class TechpackGenerator:
    @staticmethod
    def image_to_description(img_url: str, client: OpenAI = OpenAI()) -> str:
        response = client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Describe the clothing item in this image in extremely great detail. Fine enough detail that a painter would be able to recreate the exact image from the description alone."},
                        {"type": "image_url", "image_url": {"url": f"{img_url}"}},
                    ],
                }
            ],
        )
        return response.choices[0].message.content

    @staticmethod
    def tech_pack_from_description(clothing_description: str, tech_pack_section: str, client: OpenAI = OpenAI()) -> str:
        system_message = {
            "role": "system",
            "content": (f"You are a clothing designer tasked with building techpacks for clothing items that are to be sent out to manufacturers. You specialize in creating the {tech_pack_section} sections of the techpack from very detailed clothing item descriptions.")
        }
        user_message = {
            "role": "user",
            "content": f"CLOTHING DESCRIPTION: \n{clothing_description}"
        }
        messages = [system_message, user_message]
        chat_completion = client.chat.completions.create(
            messages=messages,
            model="gpt-4-turbo",
            max_tokens=1000,
        )
        return chat_completion.choices[0].message.content

    @staticmethod
    def generate_full_tech_pack(clothing_description: str, sections: List[str], client: OpenAI = OpenAI()) -> List[str]:
        tech_pack = []
        for section in sections:
            tech_pack_description = TechpackGenerator.tech_pack_from_description(clothing_description, section, client)
            tech_pack.append(tech_pack_description)
        return tech_pack
