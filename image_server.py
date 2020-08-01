import os
from datetime import datetime
from gevent.pywsgi import WSGIServer

from flask import Flask, jsonify
from keras.applications.mobilenet_v2 import MobileNetV2
from keras.preprocessing.image import img_to_array
from keras.applications.mobilenet_v2 import preprocess_input, decode_predictions
from PIL import Image
from flask import g

import sqlite3
import random
import flask
import numpy as np
import settings
import io

app = Flask(__name__)


def image_preprocessing(image, target_size):
    # if image.mode != "RGB":
    #   image = image.convert("RGB")
    img = image.resize(target_size)
    img = img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = preprocess_input(img)
    return img


def create_uuid():
    now_time = datetime.now().strftime("%Y%m%d%H%M%S")
    random_num = random.randint(0, 1000)
    unique_id = str(now_time) + str(random_num)
    return unique_id


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(settings.DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def query_db(query, args=(), one=False):
    db = get_db()
    cur = db.execute(query)
    db.commit()
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


@app.route('/')
def hello_world():
    get_db()
    return "welcome to image prediction demo!"


@app.route("/predict", methods=["POST"])
def predict():
    model = MobileNetV2(weights='imagenet')
    basedir = os.path.abspath(os.path.dirname(__file__))

    if flask.request.method == "POST":
        if flask.request.files.get("image"):
            img = flask.request.files["image"]
            path = basedir + "/static/photo/"
            file_path = path + create_uuid() + img.filename
            image = img.read()
            img.save(file_path)

            image = Image.open(io.BytesIO(image))
            image = image_preprocessing(image, (settings.IMAGE_WIDTH, settings.IMAGE_HEIGHT))
            feature = model.predict(image)
            print('Predicted:', decode_predictions(feature, top=settings.NUM_OF_PREDICTION)[0])
            return jsonify(str(decode_predictions(feature, top=settings.NUM_OF_PREDICTION)[0]))


if __name__ == '__main__':
    app.run()
    # server = WSGIServer(('0.0.0.0', 7770), app)
    # server.serve_forever()
# curl -k -X POST -F "image=@demo.jfif" -v  "http://localhost:5000/predict"
# gunicorn -c gun_config.py image_server:Flask
