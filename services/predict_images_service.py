import os
from PIL import Image

class PredictImagesService:
    def process_image(self, image):
        # Convert image to grayscale as a placeholder processing step
        img = Image.open(image)
        grayscale_img = img.convert('L')
        return grayscale_img

    def save_segmented_image(self, segmented_image):
        # Save the segmented image to the segmented_images directory
        save_path = os.path.join('/mnt/data/segmented_images', segmented_image.filename)
        segmented_image.save(save_path)
        return save_path
