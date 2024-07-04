from PIL import Image
import imagehash
from features import image_to_feature_vector

def process_image(img_path):
    try:
        img = Image.open(img_path)
        img_hash = imagehash.average_hash(img)
        features = image_to_feature_vector(img)
        return img_path, img_hash, features
    except Exception as e:
        print(f"Error processing image {img_path}: {e}")
        return img_path, None, None