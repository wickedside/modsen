import os
from PIL import Image

def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        if filename.lower().endswith(('.jpeg', '.jpg', '.png', '.bmp', '.gif')):
            img_path = os.path.join(folder, filename)
            try:
                img = Image.open(img_path)
                images.append((img, img_path))
            except (IOError, SyntaxError) as e:
                print(f"Could not open image {img_path}: {e}")
    return images