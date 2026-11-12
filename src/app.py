import flask
from config import app


@app.route('/')
def index():
    return flask.render_template('index.html')
