import os
from PIL import Image

def load_images_from_folder(folder):
    """load images from the specified folder"""
    images = []
    for filename in os.listdir(folder):
        # check if the file is an image
        if filename.lower().endswith(('.jpeg', '.jpg', '.png', '.bmp', '.gif')):
            img_path = os.path.join(folder, filename)
            try:
                # try to open the image
                img = Image.open(img_path)
                images.append((img, img_path))
            except (IOError, SyntaxError) as e:
                # print error message if the image cannot be opened
                print(f"Could not open image {img_path}: {e}")
    return images