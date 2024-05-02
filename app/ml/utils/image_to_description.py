from openai import OpenAI
from openai.types.chat.chat_completion import Choice

def image_description(img_url: str, client: OpenAI = OpenAI()) -> str:
    response = client.chat.completions.create(
    model="gpt-4-turbo",
    messages=[
        {
        "role": "user",
        "content": [
            {"type": "text", "text": "I am providing an image of a clothing item/accessory. I want you provide an item description for my store."},
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
    print(type(response.choices[0]))

    return response.choices[0]