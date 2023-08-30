from flask import Flask, Blueprint, request, jsonify
import os
import sys
from urllib.parse import urlparse

# Get the path of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from services.predict_images_service import PredictImagesService
from services.download_image import download_images_from_s3_directory
from services.upload_image import upload_directory_to_s3
print("Current Working Directory:", os.getcwd())

predict_images_blueprint = Blueprint('predict_images', __name__)
predict_service = PredictImagesService()

# Move to constant files later
local_directory = os.path.join(parent_dir, "downloaded_album")
print(local_directory)
cropped_images_directory = os.path.join(parent_dir, "cropped_images_from_the_album")
print(cropped_images_directory)
if not os.path.exists(local_directory):
    os.makedirs(local_directory)

bucket_name = "canyon-creek-cuts"



# Health check endpoint
@predict_images_blueprint.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200

@predict_images_blueprint.route('/predict', methods=['POST'])
async def predict():

    # Get the JSON data from the request
    request_data = request.json

    # Retrieve the s3_directory_url from the JSON data
    s3_directory_url = request_data.get('s3_directory_url')
    s3_folder_name= request_data.get('s3_folder')
    s3_prefix = s3_folder_name + 'Predicted_images'
    print(s3_directory_url)

    if not s3_directory_url:
        return jsonify({"error": "s3_directory_url is missing from the request data"}), 400

    # download images to the local directory from the S3 object album
    download_images_from_s3_directory(s3_directory_url, local_directory)

    # loading multiple images
    image_paths = predict_service.loading_images_paths(directory_path=local_directory)

    # Initialize the model 
    api_key = os.getenv("API_KEY")
    model = predict_service.loading_model(api_key=api_key)

    # Drawing bounding boxes based on instance segmentation prediction results
    cropped_images_paths = predict_service.bounding_boxes(model=model, image_paths=image_paths)
    # Concatenate the downloaded S3 directory and the prefix for uploading
    # Extract the prefix from the S3 URL
    #parsed_url = urlparse(s3_directory_url)
    #s3_prefix = parsed_url.path.strip('/')

    #complete_s3_prefix = f'{s3_prefix}\predictions'  # Modify this as needed
    # upload cropped images to S3 and return the S3 URLs as a list
    cropped_images_uploaded_urls = upload_directory_to_s3(cropped_images_directory, bucket_name, s3_prefix)
    #emply local 
    print(cropped_images_uploaded_urls)
    # return S3 URLs of the uploaded images
    return jsonify({'Cropped_images': cropped_images_uploaded_urls}), 200

