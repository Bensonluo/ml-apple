import os
import pymongo
import random
import flask
import numpy as np
import settings
import io

from werkzeug.http import HTTP_STATUS_CODES
from datetime import datetime
from bson.json_util import dumps
from flask import Flask, render_template, jsonify
from keras.applications.mobilenet_v2 import MobileNetV2
from keras.preprocessing.image import img_to_array
from keras.applications.mobilenet_v2 import preprocess_input, decode_predictions
from PIL import Image

app = Flask(__name__)


def image_preprocessing(image, target_size):
    img = image.resize(target_size)
    img = img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = preprocess_input(img)
    return img


# creat a unique name for image that will be stored
def create_uuid():
    now_time = datetime.now().strftime("%Y%m%d%H%M%S")
    random_num = random.randint(0, 1000)
    unique_id = str(now_time) + str(random_num)
    return unique_id


def api_abort(code, message=None, **kwargs):
    if message is None:
        message = HTTP_STATUS_CODES.get(code, '')

    response = jsonify(message=message, **kwargs)
    return response, code


# convert tuple result to dict
def tuple_to_dict(results):
    for index in range(len(results)):
        res = {
            "class_name": results[index][0],
            "class_description": results[index][1],
            "score": str(results[index][2])
        }
        results[index] = res

    return results


# connect mongoDB
client = pymongo.MongoClient(host=settings.MONGODB_HOST,
                             port=settings.MONGODB_PORT)
db = client["image_classification"]
collection = db["results"]
# collection.delete_many({})  # warning: purge database


# history page
@app.route('/')
def web_application():
    return render_template("index.html")


# endpoint that predicts received image
@app.route('/predict', methods=["POST"])
def predict():
    model = MobileNetV2(weights='imagenet')
    basedir = os.path.abspath(os.path.dirname(__file__))

    if flask.request.method == "POST":
        if flask.request.files.get("image"):
            img = flask.request.files["image"]
            path = basedir + "/static/photo/"
            file_name = create_uuid() + img.filename
            file_path = path + file_name

            image = img.read()
            image = Image.open(io.BytesIO(image))
            image.save(file_path)
            image = image_preprocessing(image,
                                        (settings.IMAGE_WIDTH,
                                         settings.IMAGE_HEIGHT))
            feature = model.predict(image)
            result = decode_predictions(feature, top=settings.NUM_OF_PREDICTION)[0]

            value = {
                "image_url": str(file_name),
                "prediction_result": tuple_to_dict(result)
            }

            collection.insert_one(value)
            return dumps(value)
        return api_abort(400)
    return api_abort(400)


# return all prediction history in the mongoDB
@app.route('/history')
def history():
    results = collection.find()
    return dumps(results)


if __name__ == '__main__':
    app.run()
