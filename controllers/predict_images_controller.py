from flask import Blueprint, request, jsonify
from services.predict_images_service import PredictImagesService

predict_images_blueprint = Blueprint('predict_images', __name__)
predict_service = PredictImagesService()

# Read the API key from the secret_key.txt file
with open('E:\\repo\Image_Extraction_yolov5_image_segmentation\secret_key.txt', 'r') as file:
    secret_key = file.read().strip()

path_file = "Image_Extraction_yolov5_image_segmentation\paths.txt"

# Read the content of the file
with open(path_file, "r") as file:
    directory_path = file.read().strip()

@predict_images_blueprint.route('/predict', methods=['POST'])
def predict():
    # Placeholder logic for prediction
    # image = request.files.get('image')
    # processed_image = predict_service.process_image(image)
    # loading multiple images
    image_paths = predict_service.loading_images_paths(directory_path=directory_path)
    # Initialize the model 
    model = predict_service.loading_model(api_key=secret_key)
    # Drawing bounding boxes based on instance segmentation prediction results
    cropped_images_directory  = predict_service.bounding_boxes(model=model, image_paths=image_paths)
    # save_path = predict_service.save_segmented_image(processed_image)
    # return jsonify({"message": "Image processed successfully", "path": save_path})
    pass