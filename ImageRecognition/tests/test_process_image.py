import unittest
from unittest.mock import patch
import os
import tempfile
from PIL import Image
import numpy as np
from ImageRecognition.image_processing.hash_images import process_image
from ImageRecognition.model.model import initialize_model

class TestProcessImage(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # model init one time for all tests
        initialize_model()

    @patch('ImageRecognition.image_processing.features.image_to_feature_vector')
    def test_process_image(self, mock_image_to_feature_vector):
        mock_image_to_feature_vector.return_value = np.random.rand(512)

        with tempfile.TemporaryDirectory() as temp_dir:
            img_path = os.path.join(temp_dir, 'test_image.jpg')
            with Image.new('RGB', (10, 10)) as img:
                img.save(img_path)

            path, img_hash, features = process_image(img_path)
            self.assertEqual(path, img_path)
            self.assertIsNotNone(img_hash)
            self.assertIsNotNone(features)
            self.assertEqual(len(features), 512)

            with Image.open(img_path) as img:
                img.close()
            os.remove(img_path)

if __name__ == '__main__':
    unittest.main()
