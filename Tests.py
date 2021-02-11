import unittest
from generator import generate_font_image


class Tester(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_get_font(self):
        # TODO
        for i in range(3):
            generate_font_image().show()