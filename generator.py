from PIL import *
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import tqdm
import logging

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger("broadcast")

txt = Image.open("im.png")
fnt = ImageFont.truetype("20352.otf", 36)
d = ImageDraw.Draw(txt)

text = '123456 Алекс'
d.text((100, 40), text, font=fnt, fill=(0, 0, 0, 255))
del d
txt.save("file.png", "PNG")
img = open('file.png', 'rb')


def crop(image_name, size):
    image = Image.open(image_name)
    width, height = image.size
    size_x, size_y = size
    num_x = width // size_x
    num_y = height // size_y
    for x in range(num_x):
        for y in range(num_y):
            cropped = image.crop((x * size_x, y * size_y, (num_x - 2) * size_x, (num_y - 2) * size_y))
            log.debug((x * size_x, y * size_y, (num_x - 2) * size_x, (num_y - 2) * size_y))
            log.debug(image.size)
            yield cropped


get_cropped_font = crop("FONT.jpg", (100, 10))
font = next(get_cropped_font)

d = ImageDraw.Draw(font)
d.text((100, 40), text, font=fnt, fill=(0, 0, 0, 255))
font.save("res.jpg")
