from flask import Flask, send_file, jsonify
from flask_restful import Api, Resource, reqparse
import random
from generator import generate
from captcha_storeger import Storeger

app = Flask(__name__)
api = Api(app)

path_to_image = "/picture/"
host = "127.0.0.1"
port = 5000


class GetCaptcha(Resource):
    def get(self):
        image_name, image_text = storager.save_captcha()
        return jsonify({"name": image_name,
                        "link": host + ":" + str(port) + path_to_image + image_name,
                        "answer": image_text})


class PictureShower(Resource):
    def get(self, name):
        return send_file("pics/" + name, mimetype='image/png')


class CheckCaptcha(Resource):
    def get(self):
        pass  # TODO


if __name__ == '__main__':
    storager = Storeger()
    api.add_resource(GetCaptcha, "/generate")
    api.add_resource(PictureShower, path_to_image + "<string:name>")
    app.run(debug=True, host=host, port=port)
