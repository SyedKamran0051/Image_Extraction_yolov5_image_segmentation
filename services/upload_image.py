import os
from dotenv import load_dotenv
import boto3

# Load environment variables from .env file
load_dotenv()

# Function to upload files to S3 using environment variables from .env
def upload_to_s3(file_path, bucket_name, object_name):
    aws_access_key = os.environ.get('AWS_ACCESS_KEY_ID')
    aws_secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')

    if aws_access_key is None or aws_secret_key is None:
        raise ValueError("AWS access key and secret access key not found in environment variables.")

    s3 = boto3.client(
        's3',
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key
    )

    s3.upload_file(file_path, bucket_name, object_name)


upload_to_s3("E:\\repo\Image_Extraction_yolov5_image_segmentation\prediction.jpg", "canyon-creek-cuts", "Predicted_images/pred_1.jpg")