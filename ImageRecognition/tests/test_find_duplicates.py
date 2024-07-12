import unittest
import os
import tempfile
from PIL import Image
from ImageRecognition.utils.find_duplicates import find_duplicates
from ImageRecognition.model.model import initialize_model

class TestFindDuplicates(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # model init one time for all tests
        initialize_model()

    def test_find_duplicates(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            img1_path = os.path.join(temp_dir, 'img1.jpg')
            img2_path = os.path.join(temp_dir, 'img2.jpg')
            img3_path = os.path.join(temp_dir, 'img3.jpg')

            Image.new('RGB', (10, 10)).save(img1_path)
            Image.new('RGB', (10, 10)).save(img2_path)
            Image.new('RGB', (10, 10)).save(img3_path)

            images = [
                (Image.open(img1_path), img1_path),
                (Image.open(img2_path), img2_path),
                (Image.open(img3_path), img3_path)
            ]

            for img in images:
                img[0].close()

            images = [
                (Image.open(img1_path), img1_path),
                (Image.open(img2_path), img2_path),
                (Image.open(img3_path), img3_path)
            ]

            hash_duplicates, feature_duplicates = find_duplicates(images)

            # т.к. изображения одинаковые, они должны быть дубликатами
            self.assertTrue(any(len(dup) > 1 for dup in hash_duplicates))
            self.assertTrue(any(len(dup) > 1 for dup in feature_duplicates))

            for img in images:
                img[0].close()

if __name__ == '__main__':
    unittest.main()
