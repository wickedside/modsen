import os
import numpy as np
from PIL import Image
import imagehash
import matplotlib.pyplot as plt
from collections import defaultdict
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import Model
from tensorflow.keras.layers import GlobalAveragePooling2D

# подрубаем предобученную модель VGG16
base_model = VGG16(weights='imagenet', include_top=False)
model = Model(inputs=base_model.input, outputs=GlobalAveragePooling2D()(base_model.output))

def load_images_from_folder(folder):
    """загружаем картинки из указанной папки"""
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

def image_to_feature_vector(img, model):
    """делаем из картинки вектор признаков с помощью модели"""
    img = img.resize((224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)
    features = model.predict(img_array)
    return features.flatten()

def find_duplicates(images):
    """ищем дубликаты картинок по хэшам и признакам"""
    hash_dict = defaultdict(list)
    feature_dict = defaultdict(list)

    for img, path in images:
        # считаем хэш картинки
        img_hash = imagehash.average_hash(img)
        hash_dict[img_hash].append(path)

        # извлекаем признаки картинки
        try:
            features = image_to_feature_vector(img, model)
            feature_dict[tuple(features)].append(path)
        except Exception as e:
            print(f"Error processing image {path}: {e}")

    # дубликаты по хэшам
    hash_duplicates = [paths for paths in hash_dict.values() if len(paths) > 1]
    # дубликаты по признакам
    feature_duplicates = [paths for paths in feature_dict.values() if len(paths) > 1]

    return hash_duplicates, feature_duplicates

def display_duplicates(duplicates):
    """показываем найденные дубликаты"""
    for dup in duplicates:
        fig, axes = plt.subplots(1, len(dup), figsize=(15, 5))
        if len(dup) == 1:
            axes = [axes]
        for ax, img_path in zip(axes, dup):
            img = Image.open(img_path)
            ax.imshow(img)
            ax.set_title(os.path.basename(img_path))
            ax.axis('off')
        plt.show()

def main(folder1, folder2=None):
    # загружаем картинки из первой папки
    images1 = load_images_from_folder(folder1)
    if folder2:
        # если есть вторая папка, загружаем и из неё
        images2 = load_images_from_folder(folder2)
        all_images = images1 + images2
    else:
        all_images = images1

    # ищем дубликаты
    hash_duplicates, feature_duplicates = find_duplicates(all_images)

    # выводим результаты
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

    # парсим аргументы командной строки
    parser = argparse.ArgumentParser(description='Find duplicate images in folders.')
    parser.add_argument('folder1', type=str, help='Path to the first folder with images.')
    parser.add_argument('folder2', type=str, nargs='?', default=None, help='Path to the second folder with images (optional).')
    args = parser.parse_args()
    main(args.folder1, args.folder2)