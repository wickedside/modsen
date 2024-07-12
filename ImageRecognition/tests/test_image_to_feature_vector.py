import unittest
from PIL import Image
from ImageRecognition.image_processing.features import image_to_feature_vector
from ImageRecognition.model.model import initialize_model

class TestImageToFeatureVector(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # model init one time for all tests
        initialize_model()

    def test_image_to_feature_vector(self):
        # creating temp img
        img = Image.new('RGB', (10, 10))
        features = image_to_feature_vector(img)
        self.assertEqual(len(features), 512)
        img.close()

if __name__ == '__main__':
    unittest.main()
