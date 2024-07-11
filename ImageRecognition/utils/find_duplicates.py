from collections import defaultdict
from multiprocessing import Pool, cpu_count
from ImageRecognition.image_processing.hash_images import process_image
from ImageRecognition.model.model import initialize_model


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