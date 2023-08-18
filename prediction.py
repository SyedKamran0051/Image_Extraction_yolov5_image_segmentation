from flask import Flask, request, jsonify
import os
import cv2
from roboflow import Roboflow
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Read the API key from the secret_key.txt file
with open('E:\\repo\Image_Extraction_yolov5_image_segmentation\secret_key.txt', 'r') as file:
    api_key = file.read().strip()

# Initialize Roboflow
rf = Roboflow(api_key=api_key)
project = rf.workspace().project("image_extraction-6dog0")
model = project.version(3).model

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200

@app.route('/predict', methods=['POST'])
async def predict_image():
    # Check if the request contains the "image_path" query parameter
    print(request.json)
      # Check if the request contains the "image_path" key in the JSON payload
    if 'image_path' not in request.json:
        return jsonify({'error': 'No image path provided'}), 400

    image_path = request.json.get('image_path')
    if not image_path:
        return jsonify({'error': 'Invalid image path provided'}), 400

    # Load the original image
    image = cv2.imread(image_path)
    if image is None:
        return jsonify({'error': 'Failed to load image'}), 400

    # Perform prediction
    response = model.predict(image_path).json()

    # Access the predictions directly
    predictions = response['predictions']

    # Process and save the segmented images
    segmented_images_paths = []
    for idx, prediction in enumerate(predictions):
        # Extract the points for the segmentation mask
        points = [(p['x'], p['y']) for p in prediction['points']]

        # Calculate the bounding box coordinates
        x_min = int(min(points, key=lambda p: p[0])[0])
        x_max = int(max(points, key=lambda p: p[0])[0])
        y_min = int(min(points, key=lambda p: p[1])[1])
        y_max = int(max(points, key=lambda p: p[1])[1])

        # Crop the segmented image based on the bounding box coordinates
        cropped_image = image[y_min:y_max, x_min:x_max]

        # Save the segmented image
        save_path = os.path.join("temp", f"segmented_image_{idx}.jpg")
        cv2.imwrite(save_path, cropped_image)
        segmented_images_paths.append(save_path)

    return jsonify({'segmented_images': segmented_images_paths}), 200

if __name__ == '__main__':
    app.run(debug=True)
