import uuid
import time
import generator
import os

time_to_live = 25

class Storeger:
    def __init__(self):
        self.data = []

    def __generate_name(self):
        name = str(uuid.uuid4()) + ".jpg"
        self.data.append({"name":name, "time": time.time()})
        return name

    def save_captcha(self):
        self.clean_waste()  # TODO Optimize
        image, image_text = generator.generate()
        image_name = self.__generate_name()
        image.save(image_name, "PNG")
        return image_name, image_text

    def clean_waste(self):
        new_data = []
        for i, image_data in enumerate(self.data):
            if time.time() - image_data["time"]>= time_to_live:
                # If we found long time ago gene    rated image - delete it and delete it's data
                os.remove(image_data["name"])
            else:
                new_data.append(image_data[i])
        self.data = new_data
