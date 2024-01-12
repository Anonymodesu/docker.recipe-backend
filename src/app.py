from flask import Flask

from util import get_recipes

app = Flask(__name__)


@app.route("/health")
def healthcheck():
    return "OK"


@app.route("/recipes")
def recipes():
    return get_recipes()
