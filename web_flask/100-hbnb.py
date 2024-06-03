#!/usr/bin/python3
"""a script that starts a Flask web application"""
from flask import Flask, abort, render_template
from models import storage


app = Flask(__name__)


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """list of all State objects in DBStorage sorted by name (A->Z)"""
    states = storage.all("State")
    amenities = storage.all("Amenity")
    places = storage.all('Place')
    return render_template('100-hbnb.html',
                           states=states, amenities=amenities, places=places)


@app.teardown_appcontext
def teardown(exception):
    """remove the current SQLAlchemy Session"""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
