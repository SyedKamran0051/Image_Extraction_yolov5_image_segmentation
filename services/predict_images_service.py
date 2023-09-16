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

        api_key = os.getenv("API_KEY")


        # Initialize Roboflow
        rf = Roboflow(api_key=api_key)
        project = rf.workspace().project("image_extraction-6dog0")
        model = project.version(3).model

        return model

    def bounding_boxes(self, model, image_paths, target_size=(2500,2500)):
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
            # Calculate new dimensions while maintaining aspect ratio
            original_height, original_width = image.shape[:2]
            target_width, target_height = target_size

            aspect_ratio = original_width / original_height
            new_width = int(target_height * aspect_ratio)
            new_height = target_height

            # Choose a high-quality interpolation method (Lanczos)
            interpolation_method = cv2.INTER_LANCZOS4

            # Resize the image while maintaining aspect ratio
            resized_image = cv2.resize(image, (new_width, new_height), interpolation=interpolation_method)

            # Save the resized image temporarily to a new path
            temp_resized_image_path = "/home/ec2-user/creekcut/Image_Extraction_yolov5_image_segmentation/temp/resized_image.jpg"
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
                save_path = os.path.join("/home/ec2-user/creekcut/Image_Extraction_yolov5_image_segmentation/cropped_images_from_the_album", segmented_image_name)
                cv2.imwrite(save_path, cropped_image)
                segmented_images_paths.append(save_path)

            os.remove(temp_resized_image_path)

        return segmented_images_paths
