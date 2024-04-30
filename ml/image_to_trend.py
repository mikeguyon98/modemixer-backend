from openai import OpenAI
from openai.types.chat.chat_completion import Choice


def generate_trend_summary(img_url: str, client: OpenAI = OpenAI()) -> Choice:
    """
    Generate a trend summary based on the image of a celebrity.

    This function sends a chat completion request to the OpenAI API with a prompt asking to describe the fashion trends
    in the image and the clothing items the celebrity is wearing.

    Args:
        img_url (str): The URL of the image.
        client (OpenAI, optional): The OpenAI client. Defaults to OpenAI().

    Returns:
        Choice: The response from the OpenAI API. 
                intputs: 
                    finish_reason, 
                    index, 
                    logprobs,
                    message: ChatCompletionMessage(content, role, function_call, tool_calls)
    example use:
        resp = generate_trend_summary("https://modemixer-images.s3.amazonaws.com/testing_image.jpg")
        text = resp.message.content
    """    
    print(img_url)
    response = client.chat.completions.create(
    model="gpt-4-turbo",
    messages=[
        {
        "role": "user",
        "content": [
            {"type": "text", "text": "I am providing an image of a celebrity. I want you to extract from each each item of clothing he is wearing along with a description. I also want you to describe the fashion trends being displayed."},
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

resp = generate_trend_summary("https://modemixer-images.s3.amazonaws.com/testing_image.jpg")
print(resp.message.content)