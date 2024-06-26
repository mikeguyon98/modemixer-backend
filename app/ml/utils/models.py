import os
import openai
from typing import List, Dict, Any

def call_dbrx(messages: List[Dict[str, Any]]) -> str:
    DATABRICKS_TOKEN = os.environ.get("DATABRICKS_TOKEN")
    client = openai.OpenAI(
        api_key=DATABRICKS_TOKEN,
        base_url="https://dbc-47b29bb9-5648.cloud.databricks.com/serving-endpoints"
    )
    chat_completion = client.chat.completions.create(
        messages=messages,
        model="databricks-dbrx-instruct",
        max_tokens=2000,
        )
            
    return chat_completion.choices[0].message.content

def call_gpt_4_turbo(messages: List[Dict[str, Any]]) -> str:
    client = openai.OpenAI()
    chat_completion = client.chat.completions.create(
        messages=messages,
        model="gpt-4-turbo",
        max_tokens=1000,
        )
            
    return chat_completion.choices[0].message.content