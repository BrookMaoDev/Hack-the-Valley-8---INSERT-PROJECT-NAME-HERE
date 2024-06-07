from flask import Flask, render_template
import tensorflow as tf
import tensorflow_datasets as tfds

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


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/demo")
def demo():
    return render_template("model_demo.html")
