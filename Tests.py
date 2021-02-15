import unittest
from generator import generate_font_image, generate_random_word, do_image_dim
from PIL import Image

class Tester(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_get_font(self):
        # TODO
        for i in range(5555):
            generate_font_image()

    def test_generate_random_word(self):
        for i in range(50):
            print(str(generate_random_word()))

    def test_do_image_dim(self):
        im = Image.open("background.jpg")
        do_image_dim(im).show()