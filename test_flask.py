from flask import Flask, request, render_template
import pickle

app = Flask(__name__)

model = pickle.load(open(''))

@app.route('/')
def home():
    return render_template('')

@app.route()
def predict():
    