import unittest
from main import load_images_from_folder, find_duplicates, image_to_feature_vector


class TestImageDuplicateFinder(unittest.TestCase):

    def test_load_images(self):
        images = load_images_from_folder('path/to/test/folder')
        self.assertGreater(len(images), 0)

    def test_find_duplicates(self):
        images = load_images_from_folder('path/to/test/folder')
        hash_duplicates, feature_duplicates = find_duplicates(images)
        self.assertIsInstance(hash_duplicates, list)
        self.assertIsInstance(feature_duplicates, list)

    def test_image_to_feature_vector(self):
        img = Image.open('path/to/test/image.jpg')
        features = image_to_feature_vector(img, model)
        self.assertEqual(len(features), 512)


if __name__ == '__main__':
    unittest.main()
