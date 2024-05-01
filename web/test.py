import requests
from bs4 import BeautifulSoup


def get_image_urls(keyword, total_images):
    # Construct the URL for the Bing image search
    search_url = f"https://www.bing.com/images/search?q={keyword.replace(' ', '+')}"

    # Perform the HTTP request
    response = requests.get(search_url)

    # Raise an exception if the request was unsuccessful
    response.raise_for_status()

    # Use BeautifulSoup to parse the HTML content
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all <a> elements with image URLs
    links = soup.find_all("a", class_="iusc")

    # Initialize a list to store the image URLs
    image_urls = []

    # Loop through all found <a> elements
    for link in links:
        # Convert the m attribute from JSON-like string to dictionary
        m = eval(link["m"])

        # Extract the image URL if it starts with 'https' and ends with '.jpg'
        image_url = m["murl"]
        if image_url.startswith("https") and image_url.lower().endswith(".jpg"):
            image_urls.append(image_url)

        # Stop if we have collected the desired number of images
        if len(image_urls) >= total_images:
            break

    return image_urls


# Example usage
urls = get_image_urls("zendeya", 4)
print(urls)
