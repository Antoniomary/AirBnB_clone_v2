#!/usr/bin/python3
"""a script that starts a Flask web application"""
from flask import Flask, abort, render_template
from models import storage


app = Flask(__name__)


@app.route("/states", strict_slashes=False)
def show_states():
    """list of all State objects in DBStorage sorted by name (A->Z)"""
    states = storage.all("State")
    return render_template('9-states.html', states=states, with_id=False)


@app.route("/states/<id>", strict_slashes=False)
def show_state_and_cities(id):
    """shows a particular state and its list of cities linked to it"""
    states = storage.all("State")
    state = states.get('State.' + id, None)
    return render_template('9-states.html', states=state, with_id=True)


@app.teardown_appcontext
def teardown(exception):
    """remove the current SQLAlchemy Session"""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
