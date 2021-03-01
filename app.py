import time

from flask import Flask, send_file, jsonify, request
from flask_restful import Api, Resource, reqparse
import random
from generator import generate
from captcha_storeger import Storeger
from database import DataBase
import logging

log = logging.getLogger("db")


app = Flask(__name__)
api = Api(app)

path_to_image = "/picture/"
host = "127.0.0.1"
port = 5000


class GetCaptcha(Resource):
    def get(self):
        key = request.args["key"]
        if db.do_some_action(key=key, action="get_captcha"):
            image_name, image_text = storager.save_captcha()
            log.debug(f"requested {time.time()}")
            return jsonify({"name": image_name,
                            "link": host + ":" + str(port) + path_to_image + image_name,
                            "answer": image_text})
        else:
            return 403


class PictureShower(Resource):
    def get(self, name):
        return send_file("pics/" + name, mimetype='image/png')


class CheckCaptcha(Resource):
    def get(self):
        pass  # TODO


if __name__ == '__main__':
    # TODO Delete all pics when start
    db = DataBase()
    storager = Storeger()
    api.add_resource(GetCaptcha, "/generate")
    api.add_resource(PictureShower, path_to_image + "<string:name>")
    app.run(debug=True, host=host, port=port)
