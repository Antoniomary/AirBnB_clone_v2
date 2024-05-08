#!/usr/bin/python3
"""a script that starts a Flask web application"""
from flask import Flask, abort, render_template
from models import storage


app = Flask(__name__)


@app.route("/states_list", strict_slashes=False)
def show_states():
    """list of all State objects in DBStorage sorted by name (A->Z)"""
    states = storage.all("State")
    states = list(states.values())
    return render_template('7-states_list.html', states=states)


@app.teardown_appcontext
def teardown(exception):
    """remove the current SQLAlchemy Session"""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
