from PIL import *
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import tqdm
import logging

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger("broadcast")

font_image = "background.jpg"
text_font = "font.otf"
text_size = 36


def crop(image_name, size):
    image = Image.open(image_name)
    width, height = image.size
    size_x, size_y = size
    num_x = width // size_x
    num_y = height // size_y
    for x in range(num_x):
        for y in range(num_y):
            sizes_to_crop = (size_x * x, size_y * y, size_x * (x + 1), size_y * (y + 1))
            log.debug(sizes_to_crop)
            cropped = image.crop(sizes_to_crop)
            yield cropped


get_cropped_font = crop("background.jpg", (256, 128))


def generate_font_image():
    font = next(get_cropped_font)
    return font


if __name__ == '__main__':
    for i in range(3):
        generate_font_image().show()
