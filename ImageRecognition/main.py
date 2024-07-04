import os
import numpy as np
from PIL import Image
import imagehash
import matplotlib.pyplot as plt
from collections import defaultdict
from multiprocessing import Pool, cpu_count
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import Model
from tensorflow.keras.layers import GlobalAveragePooling2D
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk

# initialize the model as a global variable
model = None

def initialize_model():
    global model
    # load the VGG16 model without the top layer
    base_model = VGG16(weights='imagenet', include_top=False)
    # create a new model that outputs global average pooling of the VGG16 output
    model = Model(inputs=base_model.input, outputs=GlobalAveragePooling2D()(base_model.output))

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

def image_to_feature_vector(img):
    """convert an image to a feature vector using the model"""
    # resize the image to 224x224
    img = img.resize((224, 224))
    # convert the image to an array
    img_array = image.img_to_array(img)
    # expand the dimensions to match the model input
    img_array = np.expand_dims(img_array, axis=0)
    # preprocess the image array
    img_array = preprocess_input(img_array)
    # predict the features using the model
    features = model.predict(img_array)
    return features.flatten()

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

def find_duplicates(images):
    """find duplicate images based on hashes and features"""
    hash_dict = defaultdict(list)
    feature_dict = defaultdict(list)

    # process images in batches
    batch_size = 64
    for i in range(0, len(images), batch_size):
        batch = images[i:i+batch_size]
        # use multiprocessing to process images in parallel
        with Pool(cpu_count(), initializer=initialize_model) as pool:
            results = pool.map(process_image, [img[1] for img in batch])

        for path, img_hash, features in results:
            if img_hash is not None:
                hash_dict[img_hash].append(path)
            if features is not None:
                feature_dict[tuple(features)].append(path)

    # find duplicates based on hashes
    hash_duplicates = [paths for paths in hash_dict.values() if len(paths) > 1]
    # find duplicates based on features
    feature_duplicates = [paths for paths in feature_dict.values() if len(paths) > 1]

    return hash_duplicates, feature_duplicates

def display_duplicates(duplicates):
    """display the found duplicates"""
    fig, axes = plt.subplots(1, 2, figsize=(15, 5))
    index = 0

    def update_display():
        for ax in axes:
            ax.clear()
        if duplicates:
            for ax, img_path in zip(axes, duplicates[index]):
                img = Image.open(img_path)
                ax.imshow(img)
                ax.set_title(os.path.basename(img_path))
                ax.axis('off')
        fig.canvas.draw_idle()

    def custom_forward(*args):
        nonlocal index
        index = (index + 1) % len(duplicates)
        update_display()

    def custom_back(*args):
        nonlocal index
        index = (index - 1) % len(duplicates)
        update_display()

    # monkey patch the forward and back buttons
    NavigationToolbar2Tk.forward = custom_forward
    NavigationToolbar2Tk.back = custom_back

    update_display()
    plt.show()

def main(folder1, folder2=None):
    # load images from the first folder
    images1 = load_images_from_folder(folder1)
    if folder2:
        # if there is a second folder, load images from it as well
        images2 = load_images_from_folder(folder2)
        all_images = images1 + images2
    else:
        all_images = images1

    # find duplicates
    hash_duplicates, feature_duplicates = find_duplicates(all_images)

    # print and display the results
    if hash_duplicates:
        print("Found hash duplicates:")
        for dup in hash_duplicates:
            print("\n".join(dup))
        display_duplicates(hash_duplicates)
    else:
        print("No hash duplicates found.")

    if feature_duplicates:
        print("Found feature duplicates:")
        for dup in feature_duplicates:
            print("\n".join(dup))
        display_duplicates(feature_duplicates)
    else:
        print("No feature duplicates found.")

if __name__ == "__main__":
    import argparse

    # parse command line arguments
    parser = argparse.ArgumentParser(description='Find duplicate images in folders.')
    parser.add_argument('folder1', type=str, help='Path to the first folder with images.')
    parser.add_argument('folder2', type=str, nargs='?', default=None, help='Path to the second folder with images (optional).')
    args = parser.parse_args()
    main(args.folder1, args.folder2)
