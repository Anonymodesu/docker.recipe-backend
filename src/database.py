import os

import backoff
import psycopg
from psycopg.rows import dict_row


@backoff.on_exception(backoff.constant, psycopg.OperationalError, max_tries=20)
def get_db_connection():
    return psycopg.connect(
        host=os.environ["POSTGRES_HOST"],
        dbname=os.environ["POSTGRES_DB"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
    )


def get_all_recipes():
    conn = get_db_connection()

    with conn, conn.cursor(row_factory=dict_row) as cur:
        cur.execute("SELECT name FROM recipes")
        records = [row["name"] for row in cur.fetchall()]

    return records


def get_recipes(ingredient):
    conn = get_db_connection()

    with conn, conn.cursor(row_factory=dict_row) as cur:
        cur.execute(
            """
            SELECT recipes.name
            FROM recipes
                JOIN ingredient_recipe_map
                    ON recipes.id = ingredient_recipe_map.recipe_id
                JOIN ingredients
                    ON ingredient_recipe_map.ingredient_id = ingredients.id
            WHERE LOWER(ingredients.name) = LOWER(%s)
        """,
            (ingredient,),
        )
        records = [row["name"] for row in cur.fetchall()]

    return records


def get_all_ingredients():
    conn = get_db_connection()

    with conn, conn.cursor(row_factory=dict_row) as cur:
        cur.execute("SELECT name FROM ingredients")
        records = [row["name"] for row in cur.fetchall()]

    return records


def get_ingredients(recipe):
    conn = get_db_connection()

    with conn, conn.cursor(row_factory=dict_row) as cur:
        cur.execute(
            """
            SELECT ingredients.name
            FROM ingredients
                JOIN ingredient_recipe_map
                    ON ingredients.id = ingredient_recipe_map.ingredient_id
                JOIN recipes
                    ON ingredient_recipe_map.recipe_id = recipes.id
            WHERE LOWER(recipes.name) = LOWER(%s)
        """,
            (recipe,),
        )
        records = [row["name"] for row in cur.fetchall()]

    return records
