def create_prompt(context: str, query: str) -> str:
    return f"""
CONTEXT: 
The Following is a trending celebrity outfit with similar styles to the search query:
Use the context as inspiration to generate a new outfit that is unique and stylish.
{context}

QUERY: 
{query}

DIRECTIONS:
Generate a new clothing items that matches the user query. Make sure to only include the item \
and not the person wearing it. JUST THE CLOTHING ITEM, NOTHING ELSE AND MAKE SURE IT IS NOT FOLDED. Use a plain white background for the image with nothing in the image except the clothing item. MAKE SURE THE ITEM IS HYPERREALISTIC.
"""