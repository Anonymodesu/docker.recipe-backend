from flask import Flask

from database import (get_all_ingredients, get_all_recipes, get_ingredients,
                      get_recipes)

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
def all_ingredients():
    return get_all_ingredients()


@app.route("/ingredients/<recipe>")
def ingredients(recipe):
    return get_ingredients(recipe)
