import requests
import boto3

def upload_image_s3(image_url, bucket, object_name):
    s3 = boto3.client('s3')
    response = requests.get(image_url, stream=True)
    response.raise_for_status()
    s3.upload_fileobj(response.raw, bucket, object_name)
    print(f"Uploaded {object_name} to S3 bucket {bucket}.")