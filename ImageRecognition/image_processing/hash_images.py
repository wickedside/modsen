from PIL import Image
import imagehash
from ImageRecognition.image_processing.features import image_to_feature_vector

def process_image(img_path):
    """process a single image - extract hash and features"""
    try:
        # open the image
        img = Image.open(img_path)
        # compute the image hash
        img_hash = imagehash.average_hash(img)
        # extract features using the model
        features = image_to_feature_vector(img)
        return img_path, img_hash, features
    except Exception as e:
        # print error message if the image cannot be processed
        print(f"Error processing image {img_path}: {e}")
        return img_path, None, None