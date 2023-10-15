from flask import Flask, render_template, request
import os
import random

app = Flask(__name__)

folder_path = "static/images/pistols_jpgs/"
file_names = os.listdir(folder_path)

current_index = random.randint(100, 900)
current_image = folder_path + file_names[0]


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/next_image", methods=["POST"])
def next_image():
    global current_image
    global current_index

    current_index += 1
    current_image = folder_path + file_names[current_index]

    return render_template(
        "picture_rotator.html",
        gun_exists="Gun Exists",
        image_path=current_image,
        current_image=current_image,
    )


@app.route("/prev_image", methods=["POST"])
def prev_image():
    global current_image
    global current_index

    current_index -= 1
    current_image = folder_path + file_names[current_index]

    return render_template(
        "picture_rotator.html",
        gun_exists="Gun Exists",
        image_path=current_image,
        current_image=current_image,
    )


if __name__ == "__main__":
    app.run(debug=True)
