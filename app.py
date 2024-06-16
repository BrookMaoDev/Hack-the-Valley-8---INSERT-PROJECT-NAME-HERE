from flask import Flask, render_template, request
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np
import os
import random
import logging

app = Flask(__name__)

model = tf.keras.models.load_model("model")
SAMPLE_IMAGES_DIR = "static/sample_dataset"
UPLOAD_FOLDER = "static/uploads"
EXPECTED_IMAGE_SIZE = (128, 128)

logging.basicConfig(level=logging.DEBUG)


def get_image_and_label():
    filename = random.choice(os.listdir(SAMPLE_IMAGES_DIR))
    filepath = os.path.join(SAMPLE_IMAGES_DIR, filename)
    label = "parasitized" if filename.split("_")[0] == "0" else "uninfected"
    return filepath, label


def preprocess_image(image_path: str):
    img = load_img(image_path, target_size=EXPECTED_IMAGE_SIZE)
    img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    img_array = img_array / 255.0  # Normalize the image

    return img_array


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/demo")
def demo():
    image_url, proper_label = get_image_and_label()
    img_array = preprocess_image(image_url)
    prediction = model.predict(img_array)
    confidence = tf.math.sigmoid(prediction[0][0]).numpy()

    if confidence > 0.5:
        prediction_label = "uninfected"
    else:
        prediction_label = "parasitized"
        confidence = 1 - confidence

    return render_template(
        "demo.html",
        image_url=image_url,
        proper_label=proper_label,
        prediction=prediction_label,
        confidence=confidence,
    )


@app.route("/try", methods=["GET", "POST"])
def try_it_yourself():
    logging.debug(request.files)

    if "file" not in request.files:
        logging.debug("file not in request.files")
        return render_template("try.html")

    file = request.files["file"]

    if file.filename == "":
        logging.debug('file.filename == ""')
        return render_template("try.html")

    if file:
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        img_array = preprocess_image(filepath)
        prediction = model.predict(img_array)
        logging.debug(f"prediction: {prediction}")

        confidence = tf.math.sigmoid(prediction[0][0]).numpy()
        logging.debug(f"confidence: {confidence}")

        if confidence > 0.5:
            prediction_label = "uninfected"
        else:
            prediction_label = "parasitized"
            confidence = 1 - confidence

        logging.debug(filepath)

        return render_template(
            "try.html",
            image_url=filepath,
            prediction=prediction_label,
            confidence=confidence,
        )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
