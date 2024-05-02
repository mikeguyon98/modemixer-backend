import requests

def search_images_bing(api_key, term, count=10):
    url = "https://api.bing.microsoft.com/v7.0/images/search"
    headers = {"Ocp-Apim-Subscription-Key": api_key}
    params = {"q": term, "license": "public", "imageType": "photo", "count": count}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()