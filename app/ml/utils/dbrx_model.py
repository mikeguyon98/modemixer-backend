import os
from openai import OpenAI
from typing import List, Dict, Any

def call_dbrx(messages: List[Dict[str, Any]]) -> str:
    DATABRICKS_TOKEN = os.environ.get("DATABRICKS_TOKEN")
    client = OpenAI(
        api_key=DATABRICKS_TOKEN,
        base_url="https://dbc-47b29bb9-5648.cloud.databricks.com/serving-endpoints"
    )
    chat_completion = client.chat.completions.create(
    messages=messages,
    model="databricks-dbrx-instruct",
    max_tokens=1000,
    )
            
    return chat_completion.choices[0].message.content