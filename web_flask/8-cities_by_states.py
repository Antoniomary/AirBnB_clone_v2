#!/usr/bin/python3
"""a script that starts a Flask web application"""
from flask import Flask, abort, render_template
from models import storage


app = Flask(__name__)


@app.route("/cities_by_states", strict_slashes=False)
def show_cities_by_states():
    """list of all State objects in DBStorage sorted by name (A->Z)
       and the City objects linked to the State sorted by name (A->Z)
    """
    states = storage.all("State")
    return render_template('8-cities_by_states.html', states=states)


@app.teardown_appcontext
def teardown(exception):
    """remove the current SQLAlchemy Session"""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
