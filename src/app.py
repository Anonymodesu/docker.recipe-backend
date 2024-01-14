from flask import Flask

from database import get_all_recipes, get_ingredients, get_recipes

app = Flask(__name__)


@app.route("/health")
def healthcheck():
    return "OK"


@app.route("/recipes")
def all_recipes():
    return get_all_recipes()


@app.route("/recipes/<ingredient>")
def recipes(ingredient):
    return get_recipes(ingredient)


@app.route("/ingredients")
def ingredients():
    return get_ingredients()
