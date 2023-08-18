import os
import boto3
import requests
from urllib.parse import urlparse
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def download_images_from_s3_directory(s3_directory_url, local_directory):
    # Parse the provided S3 directory URL
    parsed_url = urlparse(s3_directory_url)
    bucket_name = parsed_url.netloc
    directory_path = parsed_url.path.lstrip('/')

    # Initialize the S3 client
    s3 = boto3.client('s3')

    # List objects in the specified "directory"
    objects = s3.list_objects_v2(Bucket=bucket_name, Prefix=directory_path)

    if 'Contents' in objects:
        for obj in objects['Contents']:
            object_key = obj['Key']

            # Skip over objects that represent folders (end with '/')
            if object_key.endswith('/'):
                continue

            s3_url = f"s3://{bucket_name}/{object_key}"
            download_image_from_s3_url(s3_url, local_directory)
    else:
        print(f"No objects found in the '{directory_path}' directory.")

def download_image_from_s3_url(s3_url, local_directory):
    # Initialize the S3 resource
    s3_resource = boto3.resource('s3')

    # Extract bucket name and object key from the S3 URL
    parsed_url = urlparse(s3_url)
    bucket_name = parsed_url.netloc
    object_key = parsed_url.path.lstrip('/')

    # Build the local file path
    local_file_path = os.path.join(local_directory, os.path.basename(object_key))

    # Download the object from S3 to the local file path
    s3_resource.Bucket(bucket_name).download_file(object_key, local_file_path)

    print(f"Downloaded: {s3_url} -> {local_file_path}")