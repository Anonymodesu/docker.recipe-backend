import os
from urllib.parse import quote

import backoff
import psycopg
import pytest
import requests
import requests.exceptions
from psycopg.errors import UndefinedTable
from psycopg.rows import dict_row


@backoff.on_exception(backoff.constant, psycopg.OperationalError, max_tries=20)
def get_db_connection():
    return psycopg.connect(
        host=os.environ["POSTGRES_HOST"],
        dbname=os.environ["POSTGRES_DB"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
    )


@backoff.on_exception(
    backoff.constant, requests.exceptions.ConnectionError, max_tries=10
)
def wait_for_webserver():
    response = requests.get("http://webserver/health").text
    assert response == "OK"


@backoff.on_exception(backoff.constant, UndefinedTable, max_tries=10)
def wait_for_database():
    conn = get_db_connection()
    with conn, conn.cursor(row_factory=dict_row) as cur:
        cur.execute("SELECT count(*) AS count FROM ingredient_recipe_map")
        assert cur.fetchone()["count"] > 1


@pytest.fixture(scope="session")
def wait_for_services():
    wait_for_database()
    wait_for_webserver()


def test_recipes(wait_for_services):
    actual_recipes = requests.get("http://webserver/recipes").json()
    assert len(actual_recipes) == 25
    assert {"Pad Thai", "Burger", "Corn Flakes Chilaquiles"} <= set(actual_recipes)


def test_ingredients_for_recipe(wait_for_services):
    actual_ingredients = requests.get(
        f"http://webserver/ingredients/{quote('Avocado Salmon Toast')}"
    ).json()
    assert set(actual_ingredients) == {
        "Avocado",
        "Bread",
        "Salmon",
        "Sour cream",
        "Yoghurt",
    }


def test_recipes_for_ingredient(wait_for_services):
    actual_recipes = requests.get("http://webserver/recipes/rice").json()
    assert set(actual_recipes) == {
        "Rice Salad",
        "Claypot Rice",
        "Tasteless fried rice",
        "Congee",
    }


def test_ingredients(wait_for_services):
    actual_ingredients = requests.get("http://webserver/ingredients").json()
    assert len(actual_ingredients) == 78
    assert {"Soy Sauce", "Aioli", "Yoghurt"} <= set(actual_ingredients)
