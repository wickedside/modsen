import unittest
from unittest.mock import patch
import os
import numpy as np
from PIL import Image
import tempfile
from main import (
    load_images_from_folder,
    image_to_feature_vector,
    process_image,
    find_duplicates,
    initialize_model
)


class TestImageDuplicateFinder(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # инициализируем модель один раз для всех тестов
        initialize_model()

    def test_load_images_from_folder(self):
        # создаем временную директорию и несколько изображений
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

    def test_image_to_feature_vector(self):
        # создаем временное изображение
        img = Image.new('RGB', (10, 10))
        features = image_to_feature_vector(img)
        self.assertEqual(len(features), 512)
        img.close()

    @patch('main.image_to_feature_vector')
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
