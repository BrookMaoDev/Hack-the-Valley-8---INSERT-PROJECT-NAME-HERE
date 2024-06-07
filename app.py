from flask import Flask, render_template, url_for
import tensorflow as tf
import tensorflow_datasets as tfds
import base64
from io import BytesIO
from PIL import Image

app = Flask(__name__)

# Set the shuffle seed to match the one used during model training
SHUFFLE_SEED = 42

# Ensuring we get only a small portion of the validation data
sample_dataset, info = tfds.load(
    name="malaria",
    split=["train[80%:81%]"],
    shuffle_files=True,
    as_supervised=True,
    with_info=True,
    read_config=tfds.ReadConfig(shuffle_seed=SHUFFLE_SEED),
)

# Extracting the class labels
class_labels = info.features["label"].int2str


# Function to get an image and its label from the dataset
def get_image_and_label():
    for image, label in sample_dataset[0].take(1):
        return image.numpy(), class_labels(label.numpy())


# Function to convert the image to base64
def image_to_base64(image):
    pil_image = Image.fromarray(image)
    buffered = BytesIO()
    pil_image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/demo")
def demo():
    image, proper_label = get_image_and_label()
    image_base64 = image_to_base64(image)
    image_url = f"data:image/png;base64,{image_base64}"

    prediction = "Parasitized"  # Hardcoded for now
    confidence = "95.45"  # Hardcoded for now

    return render_template(
        "demo.html",
        image_url=image_url,
        proper_label=proper_label,
        prediction=prediction,
        confidence=confidence,
    )


@app.route("/try")
def try_it_yourself():
    return "Try It Yourself Page"
