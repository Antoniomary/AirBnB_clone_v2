#!/usr/bin/python3
"""a script that starts a Flask web application"""
from flask import Flask, abort, render_template
from models import storage


app = Flask(__name__)


@app.route("/hbnb_filters", strict_slashes=False)
def hbnb_filters():
    """list of all State objects in DBStorage sorted by name (A->Z)"""
    states = storage.all("State")
    amenities = storage.all("Amenities")
    return render_template('/10-hbnb_filters.html',
                            states=states, amenities=amenities)


@app.teardown_appcontext
def teardown(exception):
    """remove the current SQLAlchemy Session"""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
