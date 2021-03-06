from PIL import *
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw, ImageEnhance
from PIL import ImageFilter
import tqdm
import logging

import random

import requests

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger("broadcast")

font_image_name = "background.jpg"
font_name = "font.otf"


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


def generate_random_word(length_limit: tuple = (3, 5)):
    """Generate random word form dictionary
    :param length_limit maximum length of word (min, max)
    """
    def is_word_correct(word):
        blocked_symbols = ["'", "\\", ",", "/", "!"]
        for blocked_symbol in blocked_symbols:
            if blocked_symbol in word:
                return False
            else:
                return True
    log.debug("Generating random word")
    response = requests.get("http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain",
                            headers={
                                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.7.42.7011 Safari/537.36"})
    words = response.content.splitlines()
    gen_word = str(random.choice(words)).replace("'", "")

    while (length_limit[1] < len(gen_word) < length_limit[0]) and (is_word_correct(word)):
        gen_word = str(random.choice(words)).replace("'", "")
    return gen_word[1:]


def add_text(text, image, text_font, text_colour=(205, 0, 0)):
    log.debug(f"Adding text {text} to image with colour {text_colour}")
    fontimage = Image.new('L', size)

    w, h = text_font.getsize(text=text)
    W, H = size

    ImageDraw.Draw(fontimage).text(((W-w)/2,(H-h)/2), text, fill=255, font=text_font)
    image.paste(text_colour, box=(0, 0), mask=fontimage)
    return image


def generate_optimum_fontsize(word):
    """Reduce font size untill word will be """
    f_size = 40
    fnt = ImageFont.truetype(font_name, f_size)
    length = fnt.getsize(word)
    log.debug(f"Now len = {length}, f_size = {f_size}. Trying to get opt. font size.")
    while length[0] >= size[0] - 2:
        f_size -= 2
        fnt = ImageFont.truetype(font_name, f_size)
        length = fnt.getsize(word)
    log.debug(f"Now len = {length}, f_size = {f_size}")
    return fnt


def do_image_dim(image, force=128):
    """Do image more dim"""
    log.debug("Doing font more dim")
    dimmer = ImageEnhance.Brightness(image)
    dimmed_im = dimmer.enhance(force)
    return dimmed_im


def add_image_filter(image, f, filter):
    log.debug(f"Applying filter {filter} to image")
    return image.filter(filter)


def generate():
    word = generate_random_word()
    log.info(word)
    fnt = generate_optimum_fontsize(word)
    font_image = do_image_dim(generate_font_image())
    res = add_text(word, font_image, text_font=fnt)
    return res, word
    # TODOD


if __name__ == '__main__':
    word = generate_random_word()
    log.info(word)
    fnt = generate_optimum_fontsize(word)
    font_image = do_image_dim(generate_font_image())
    res = add_text(word, font_image, text_font=fnt)
    res.save("file.png", "PNG")
    res.show()
