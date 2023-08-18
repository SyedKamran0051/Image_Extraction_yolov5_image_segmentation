import os
import cv2
from roboflow import Roboflow
from PIL import Image
import roboflow
import time
class PredictImagesService:
    def process_image(self, image):
        # Convert image to grayscale as a placeholder processing step
        img = Image.open(image)
        grayscale_img = img.convert('L')
        return grayscale_img
    
    def loading_images_paths(self, directory_path):
        image_extensions = ['.jpg']  # Add more extensions if needed
        image_paths = []

        for filename in os.listdir(directory_path):
            if any(filename.lower().endswith(ext) for ext in image_extensions):
                path = os.path.join(directory_path, filename.replace('\\', '/'))
                print("Image Path:", path)  # Print the image path
                image_paths.append(path)

        return image_paths


    def save_segmented_image(self, segmented_image):
        # Save the segmented image to the segmented_images directory
        save_path = os.path.join('/mnt/data/segmented_images', segmented_image.filename)
        segmented_image.save(save_path)
        return save_path

    def loading_model(self, api_key):
        # Read the API key from the secret_key.txt file
        with open('E:\\repo\Image_Extraction_yolov5_image_segmentation\secret_key.txt', 'r') as file:
            api_key = file.read().strip()

        # Initialize Roboflow
        rf = Roboflow(api_key=api_key)
        project = rf.workspace().project("image_extraction-6dog0")
        model = project.version(3).model

        return model
    
    def bounding_boxes(self, model, image_paths, target_size=(2000,2000)):
        segmented_images_paths = []
        for image_path in image_paths:
            print(image_path)
            # Load the original image
            image = cv2.imread(image_path)
            print(image_path)
            if image is None:
                print(f'Failed to load image: {image_path}')
                continue

            # Perform prediction
            # Resize the image
            resized_image = cv2.resize(image, target_size)

            # Save the resized image temporarily to a new path
            temp_resized_image_path = "E:\creek_cut\Image_Extraction_yolov5_image_segmentation\\temp\\resized_image.jpg"
            cv2.imwrite(temp_resized_image_path, resized_image)

            # Perform prediction using the resized image path
            response = model.predict(temp_resized_image_path).json()
            predictions = response['predictions']

            # Process and save the segmented images
            for idx, prediction in enumerate(predictions):
                # Extract the points for the segmentation mask
                points = [(p['x'], p['y']) for p in prediction['points']]

                # Calculate the bounding box coordinates
                x_min = int(min(points, key=lambda p: p[0])[0])
                x_max = int(max(points, key=lambda p: p[0])[0])
                y_min = int(min(points, key=lambda p: p[1])[1])
                y_max = int(max(points, key=lambda p: p[1])[1])

                # Crop the segmented image based on the bounding box coordinates
                cropped_image = resized_image[y_min:y_max, x_min:x_max]

                # Save the segmented image with corresponding name
                original_image_name = os.path.basename(image_path)
                segmented_image_name = f"segmented_{idx}_{original_image_name}"
                save_path = os.path.join("E:/creek_cut/Image_Extraction_yolov5_image_segmentation/cropped_images_from_the_album", segmented_image_name)
                cv2.imwrite(save_path, cropped_image)
                segmented_images_paths.append(save_path)

            os.remove(temp_resized_image_path)

        return segmented_images_paths
