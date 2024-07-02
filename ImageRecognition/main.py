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

# initialize the model as a global variable
model = None

def initialize_model():
    """initialize the vgg16 model with global average pooling"""
    global model
    base_model = VGG16(weights='imagenet', include_top=False)
    model = Model(inputs=base_model.input, outputs=GlobalAveragePooling2D()(base_model.output))

def load_images_from_folder(folder):
    """load images from the specified folder"""
    images = []
    for filename in os.listdir(folder):
        if filename.lower().endswith(('.jpeg', '.jpg', '.png', '.bmp', '.gif')):
            img_path = os.path.join(folder, filename)
            try:
                img = Image.open(img_path)
                images.append((img, img_path))
            except (IOError, SyntaxError) as e:
                print(f"could not open image {img_path}: {e}")
    return images

def image_to_feature_vector(img):
    """convert image to feature vector using the vgg16 model"""
    img = img.resize((224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)
    features = model.predict(img_array)
    return features.flatten()

def process_image(img_path):
    """process a single image to extract its hash and feature vector"""
    try:
        img = Image.open(img_path)
        img_hash = imagehash.average_hash(img)
        features = image_to_feature_vector(img)
        return img_path, img_hash, features
    except Exception as e:
        print(f"error processing image {img_path}: {e}")
        return img_path, None, None

def find_duplicates(images):
    """find duplicate images by their hashes and feature vectors"""
    hash_dict = defaultdict(list)
    feature_dict = defaultdict(list)

    # process images in batches
    batch_size = 64
    for i in range(0, len(images), batch_size):
        batch = images[i:i+batch_size]
        with Pool(cpu_count(), initializer=initialize_model) as pool:
            results = pool.map(process_image, [img[1] for img in batch])

        for path, img_hash, features in results:
            if img_hash is not None:
                hash_dict[img_hash].append(path)
            if features is not None:
                feature_dict[tuple(features)].append(path)

    # duplicates by hashes
    hash_duplicates = [paths for paths in hash_dict.values() if len(paths) > 1]
    # duplicates by features
    feature_duplicates = [paths for paths in feature_dict.values() if len(paths) > 1]

    return hash_duplicates, feature_duplicates

def display_duplicates(duplicates):
    """show found duplicates with navigation buttons"""
    fig, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.2)
    ax.set_axis_off()

    class Index:
        ind = 0

        def next(self, event):
            self.ind = (self.ind + 1) % len(duplicates)
            self.update()

        def prev(self, event):
            self.ind = (self.ind - 1) % len(duplicates)
            self.update()

        def update(self):
            ax.clear()
            ax.set_axis_off()
            dup = duplicates[self.ind]
            fig.suptitle(f'showing duplicates set {self.ind + 1} of {len(duplicates)}')
            for i, img_path in enumerate(dup):
                img = Image.open(img_path)
                ax.imshow(img)
                ax.set_title(os.path.basename(img_path))
                ax.axis('off')
            fig.canvas.draw()

    callback = Index()
    fig.canvas.mpl_connect('key_press_event', lambda event: callback.next(event) if event.key == 'right' else callback.prev(event) if event.key == 'left' else None)

    callback.update()
    plt.show()

def main(folder1, folder2=None):
    """main function to load images, find duplicates and display results"""
    # load images from the first folder
    images1 = load_images_from_folder(folder1)
    if folder2:
        # if there's a second folder, load images from it as well
        images2 = load_images_from_folder(folder2)
        all_images = images1 + images2
    else:
        all_images = images1

    # find duplicates
    hash_duplicates, feature_duplicates = find_duplicates(all_images)

    # display results
    if hash_duplicates:
        print("found hash duplicates:")
        for dup in hash_duplicates:
            print("\n".join(dup))
        display_duplicates(hash_duplicates)
    else:
        print("no hash duplicates found.")

    if feature_duplicates:
        print("found feature duplicates:")
        for dup in feature_duplicates:
            print("\n".join(dup))
        display_duplicates(feature_duplicates)
    else:
        print("no feature duplicates found.")

if __name__ == "__main__":
    import argparse

    # parse command line arguments
    parser = argparse.ArgumentParser(description='find duplicate images in folders.')
    parser.add_argument('folder1', type=str, help='path to the first folder with images.')
    parser.add_argument('folder2', type=str, nargs='?', default=None, help='path to the second folder with images (optional).')
    args = parser.parse_args()
    main(args.folder1, args.folder2)