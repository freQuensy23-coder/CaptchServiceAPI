from PIL import *
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import tqdm
import logging

import random

import requests

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger("broadcast")

font_image = "background.jpg"
text_font = fnt = ImageFont.truetype("font.otf", 40)
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


size = (256, 64)
get_cropped_font = crop("background.jpg", size)


def generate_font_image():
    font = next(get_cropped_font)
    return font


def add_text_to_image():
    pass


def generate_random_word():
    response = requests.get("http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain",
                            headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.7.42.7011 Safari/537.36"})
    WORDS = response.content.splitlines()
    word = str(random.choice(WORDS)).replace("'", "")
    return word[1:]


def add_text(text, image):
    fontimage = Image.new('L', size)
    ImageDraw.Draw(fontimage).text((0, 0), text, fill=255, font=text_font)
    image.paste((255, 0, 0), box=(0, 0), mask=fontimage)
    return image


def do_image_dim(image, force = 128):
    """Do image more dim"""
    image_size = image.size
    resulted_image = Image.new(mode="RGBA", size=image_size)
    resulted_image.paste((force, 0, 0), box=(0, 0), mask=image)
    return resulted_image


if __name__ == '__main__':
    word = generate_random_word()
    while fnt.getsize(word)[0] >= size[0]:
        log.debug(word)
        word = generate_random_word()
    log.info(word)
    res = add_text(word, generate_font_image())
    res.save("file.png", "PNG")