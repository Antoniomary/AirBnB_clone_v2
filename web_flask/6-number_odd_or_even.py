#!/usr/bin/python3
"""a script that starts a Flask web application"""
from flask import Flask, abort, render_template


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
def c_text():
    """displays C followed by the value of the text"""
    formatted_text = text.replace('_', ' ')
    return 'C ' + formatted_text


@app.route("/python", strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def python_text(text=""):
    """displays Python followed by the value of the text if any"""
    formatted_text = text.replace('_', ' ') if text else "is cool"
    return 'Python ' + formatted_text


@app.route("/number/<n>", strict_slashes=False)
def number(n=''):
    """display 'n is a number' only if n is an integer"""
    if n.isdigit():
        return f'{n} is a number'
    abort(404)


@app.route("/number_template/<n>", strict_slashes=False)
def number_template(n=''):
    """display HTML page only if n is an integer"""
    if n.isdigit():
        return render_template('5-number.html', n=n)
    abort(404)


@app.route("/number_odd_or_even/<n>", strict_slashes=False)
def odd_or_even(n=''):
    """display 'n is odd|even' only if n is an integer"""
    if n.isdigit():
        return render_template('6-number_odd_or_even.html', n=n)
    abort(404)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
