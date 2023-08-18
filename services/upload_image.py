import os
from dotenv import load_dotenv
import boto3

# Load environment variables from .env file
load_dotenv()

# Function to upload files to S3 using environment variables from .env
def upload_directory_to_s3(directory_path, bucket_name, s3_prefix):
    aws_access_key = os.environ.get('AWS_ACCESS_KEY_ID')
    aws_secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')

    if aws_access_key is None or aws_secret_key is None:
        raise ValueError("AWS access key and secret access key not found in environment variables.")

    s3 = boto3.client(
        's3',
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key
    )

    s3_urls = []

    for root, _, files in os.walk(directory_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            s3_object_key = os.path.join(s3_prefix, file_name)
            
            s3.upload_file(file_path, bucket_name, s3_object_key)
            
            s3_url = f"https://{bucket_name}.s3.amazonaws.com/{s3_object_key}"
            s3_urls.append(s3_url)
            print(s3_urls)
    
    return s3_urls
