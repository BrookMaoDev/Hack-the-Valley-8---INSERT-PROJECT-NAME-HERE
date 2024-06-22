from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.models import load_model
from numpy import expand_dims
from numpy.typing import NDArray
from os import listdir
from os.path import join, isfile
from tempfile import mkdtemp
from random import choice
from math import e

app = Flask(__name__)
model = load_model("model")

# Constants
SAMPLE_IMAGES_DIR = "static/sample_dataset"
EXPECTED_IMAGE_SIZE = (128, 128)
HEALTHY_LABEL = "healthy"
PARASITIZED_LABEL = "parasitized"


def get_image_path_and_label() -> tuple[str, str]:
    """
    Selects a random image from the sample dataset directory and determines its label.

    Returns:
        tuple[str, str]: A tuple containing the file path of the image and its label.
    """
    filename = choice(listdir(SAMPLE_IMAGES_DIR))
    filepath = join(SAMPLE_IMAGES_DIR, filename)
    label = PARASITIZED_LABEL if filename.split("_")[0] == "0" else HEALTHY_LABEL
    return filepath, label


def preprocess_image(image_path: str) -> NDArray:
    """
    Loads and preprocesses an image for model prediction.

    Args:
        image_path (str): The file path of the image to preprocess.

    Returns:
        NDArray: The preprocessed image as a numpy array.
    """
    img = load_img(image_path, target_size=EXPECTED_IMAGE_SIZE)
    img_array = img_to_array(img)
    img_array = expand_dims(img_array, axis=0)
    img_array /= 255.0  # Normalize the image to [0, 1]
    return img_array


def sigmoid(x: float) -> float:
    """
    Computes the sigmoid function for the given input.

    Args:
        x (float): The input value.

    Returns:
        float: The output of the sigmoid function.
    """
    return 1 / (1 + e**-x)


def predict(img_array: NDArray) -> dict:
    """
    Predicts the label for a given preprocessed image array.

    Args:
        img_array (NDArray): The preprocessed image array.

    Returns:
        dict: A dictionary containing the raw output, healthy probability,
              prediction label, and confidence of the prediction.
    """
    logit = model.predict(img_array)[0][0].item()
    probability_healthy = sigmoid(logit)

    if probability_healthy > 0.5:
        prediction_label = HEALTHY_LABEL
        confidence = probability_healthy
    else:
        prediction_label = PARASITIZED_LABEL
        confidence = 1 - probability_healthy

    return {
        "raw_output": logit,
        "healthy_probability": probability_healthy,
        "prediction": prediction_label,
        "confidence": confidence,
    }


@app.route("/")
def index():
    """
    Renders the main index page.
    """
    return render_template("index.html")


@app.route("/demo")
def render_demo():
    """
    Renders the demo page.
    """
    return render_template("demo.html")


@app.route("/try")
def render_try():
    """
    Renders the try page.
    """
    return render_template("try.html")


@app.route("/get-image-path-and-label")
def return_image_path_and_label():
    """
    Returns a random image path and its proper label in JSON format.
    """
    filepath, label = get_image_path_and_label()
    return {"filepath": filepath, "proper_label": label}


@app.route("/predict", methods=["POST"])
def return_prediction():
    """
    Returns the prediction for a given image file path in JSON format.
    """
    path = request.form["filepath"]

    if not isfile(path):
        return {"message": f"File does not exist: {path}"}

    img_array = preprocess_image(path)
    return predict(img_array)


@app.route("/upload-and-predict", methods=["POST"])
def upload_and_predict():
    """
    Handles image file upload, makes a prediction, and returns the result in JSON format.
    """
    if "file" not in request.files:
        return {"message": "No file part"}

    file = request.files["file"]

    if file.filename == "":
        return {"message": "No selected file"}

    filename = secure_filename(file.filename)
    temp_dir = mkdtemp()
    filepath = join(temp_dir, filename)
    file.save(filepath)

    img_array = preprocess_image(filepath)
    return predict(img_array)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
