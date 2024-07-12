import unittest
import os
import tempfile
from PIL import Image
from ImageRecognition.image_processing.load_images import load_images_from_folder

class TestLoadImagesFromFolder(unittest.TestCase):

    def test_load_images_from_folder(self):
        # creating temp dir and some images
        with tempfile.TemporaryDirectory() as temp_dir:
            img1_path = os.path.join(temp_dir, 'img1.jpg')
            img2_path = os.path.join(temp_dir, 'img2.png')

            Image.new('RGB', (10, 10)).save(img1_path)
            Image.new('RGB', (10, 10)).save(img2_path)

            images = load_images_from_folder(temp_dir)
            self.assertEqual(len(images), 2)
            self.assertTrue(any(img[1].endswith('img1.jpg') for img in images))
            self.assertTrue(any(img[1].endswith('img2.png') for img in images))

            # закрываем файлы
            for img, path in images:
                img.close()

if __name__ == '__main__':
    unittest.main()