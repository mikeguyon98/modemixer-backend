import requests
from bs4 import BeautifulSoup
import boto3


def get_image_urls(keyword, total_images):
    image_urls = []
    page = 0  # start from the first page
    while len(image_urls) < total_images:
        url = f"https://www.bing.com/images/async?q={keyword}&first={page}&count=35&adlt=off"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        images = soup.find_all("a", {"class": "iusc"})

        if not images:
            print("No more images found")
            break

        for img in images:
            try:
                img_url = eval(img["m"])["murl"]
                image_urls.append(img_url)
                if len(image_urls) >= total_images:
                    break
            except Exception as e:
                print(f"Error getting image URL: {e}")

        page += 35

    return image_urls


def upload_image_to_s3(image_url, bucket_name):
    session = boto3.Session(
        aws_access_key_id="AKIA2UC3EW36VE77IAOA",
        aws_secret_access_key="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",
        region_name="us-east-1",
    )
    s3 = session.client("s3")

    try:
        response = requests.get(image_url, stream=True)
        file_name = image_url.split("/")[-1]
        s3.upload_fileobj(response.raw, bucket_name, file_name)
        print(f"Successfully uploaded {file_name} to S3 bucket {bucket_name}")
    except Exception as e:
        print(f"Failed to upload {image_url}: {e}")


def main():
    keyword = "Gigi Hadid Recent Outfit"
    total_images = 5
    bucket_name = "modemixer-images"

    image_urls = get_image_urls(keyword, total_images)
    for image_url in image_urls:
        upload_image_to_s3(image_url, bucket_name)
    response = requests.get(image_urls[0], stream=True)


if __name__ == "__main__":
    main()
