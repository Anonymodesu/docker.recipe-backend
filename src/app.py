from flask import Flask

from util import get_ingredients, get_recipes

app = Flask(__name__)


@app.route("/health")
def healthcheck():
    return "OK"


@app.route("/recipes")
def recipes():
    return get_recipes()


@app.route("/ingredients")
def ingredients():
    return get_ingredients()
