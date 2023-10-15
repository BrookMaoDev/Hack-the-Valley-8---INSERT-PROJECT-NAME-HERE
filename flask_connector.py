from flask import Flask, render_template, request

app = Flask(__name__)

# Initialize the current_image variable
current_image = "/static/your-image.jpg"

@app.route('/')
def index():
    gun_exists = "Gun exists"  # Replace with the actual text you want to pass

    return render_template('your_template.html', gun_exists=gun_exists, image_path=current_image, current_image=current_image)

@app.route('/next_image', methods=['POST'])
def next_image():
    global current_image  # Make sure to use the global variable

    # Get the current image from the form data
    current_image = request.form['current_image']

    # Implement your logic to get the next image (update current_image)
    # For example:
    # current_image = "/static/next-image.jpg"

    return render_template('your_template.html', gun_exists="New text", image_path=current_image, current_image=current_image)

if __name__ == '__main__':
    app.run()