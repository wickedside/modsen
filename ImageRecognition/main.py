import argparse
from image_processing.load_images import load_images_from_folder
from utils.find_duplicates import find_duplicates
from image_processing.display import display_duplicates

def main(folder1, folder2=None):
    images1 = load_images_from_folder(folder1)
    if folder2:
        images2 = load_images_from_folder(folder2)
        all_images = images1 + images2
    else:
        all_images = images1

    hash_duplicates, feature_duplicates = find_duplicates(all_images)

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
    parser = argparse.ArgumentParser(description='Find duplicate images in folders.')
    parser.add_argument('folder1', type=str, help='Path to the first folder with images.')
    parser.add_argument('folder2', type=str, nargs='?', default=None, help='Path to the second folder with images (optional).')
    args = parser.parse_args()
    main(args.folder1, args.folder2)