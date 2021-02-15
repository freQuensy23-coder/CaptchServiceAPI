from PIL import *
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw, ImageEnhance
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
    """Crop image. Return generator, that will give u each rectangle of the picture"""
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
    """Generating new font image. If we have already used all the background images, open again."""
    global get_cropped_font
    try:
        font = next(get_cropped_font)
    except StopIteration:
        del get_cropped_font
        get_cropped_font = crop("background.jpg", size)
        font = next(get_cropped_font)
    return font


def generate_random_word(length_limit: tuple = (2, 8)):
    """Generate random word form dictionary
    :param length_limit maximum length of word (min, max)
    """
    response = requests.get("http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain",
                            headers={
                                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.7.42.7011 Safari/537.36"})
    words = response.content.splitlines()
    gen_word = str(random.choice(words)).replace("'", "")

    while length_limit[1] < len(word) < length_limit[0]:
        gen_word = str(random.choice(words)).replace("'", "")

    return word[1:]


def add_text(text, image, text_colour=(205, 0, 0)):
    fontimage = Image.new('L', size)
    ImageDraw.Draw(fontimage).text((0, 0), text, fill=255, font=text_font)
    image.paste(text_colour, box=(0, 0), mask=fontimage)
    return image


def do_image_dim(image, force=128):
    """Do image more dim"""
    dimmer = ImageEnhance.Brightness(image)
    dimmed_im = dimmer.enhance(force)
    return dimmed_im


if __name__ == '__main__':
    word = generate_random_word()
    while fnt.getsize(word)[0] >= size[0]:
        log.debug(word)
        word = generate_random_word()
    log.info(word)
    res = add_text(word, do_image_dim(generate_font_image()))
    res.save("file.png", "PNG")
