#!/usr/bin/python3
"""a script that starts a Flask web application"""
from flask import Flask


app = Flask(__name__)


@app.route("/", strict_slashes=False)
def index():
    """displays Hello HBNB! as default index page"""
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """displays HBNB"""
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def display_c_text(text):
    """displays C followed by the value of the text"""
    formatted_text = text.replace('_', ' ')
    return 'C ' + formatted_text


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
