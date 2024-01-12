from __future__ import annotations

import csv
import logging
import os

import psycopg

from util import get_db_connection


def generate_table_values(csv_file: str):
    ingredient_recipe_pairs = []
    ingredient_id_map = {}
    recipe_id_map = {}

    with open(csv_file) as f:
        reader = csv.DictReader(f)

        for i, recipe in enumerate(reader.fieldnames):
            if recipe != "Ingredients":
                recipe_id_map[recipe] = i

        for i, row in enumerate(reader):
            ingredient = row["Ingredients"]
            recipes = set(row.keys()) - {"Ingredients"}

            ingredient_id_map[ingredient] = i
            for recipe in recipes:
                if row[recipe].upper().strip() == "X":
                    ingredient_recipe_pairs.append(
                        (ingredient_id_map[ingredient], recipe_id_map[recipe])
                    )

    return ingredient_id_map, recipe_id_map, ingredient_recipe_pairs


def create_tables(
    db_connection: psycopg.Connection,
    ingredient_id_map: dict[str, int],
    recipe_id_map: dict[str, int],
    ingredient_recipe_pairs: list[tuple[str, str]],
):
    with db_connection, db_connection.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE ingredients (
                id      int         PRIMARY KEY,
                name    varchar(40) UNIQUE
            );

            CREATE TABLE recipes (
                id      int         PRIMARY KEY,
                name    varchar(40) UNIQUE
            );

            CREATE TABLE ingredient_recipe_map (
                ingredient_id   int REFERENCES ingredients(id),
                recipe_id       int REFERENCES recipes(id),
                PRIMARY KEY(ingredient_id, recipe_id)
            );
            """
        )

        cur.executemany(
            "INSERT INTO ingredients (name, id) VALUES (%s, %s)",
            ingredient_id_map.items(),
        )

        cur.executemany(
            "INSERT INTO recipes (name, id) VALUES (%s, %s)", recipe_id_map.items()
        )

        cur.executemany(
            "INSERT INTO ingredient_recipe_map "
            "(ingredient_id, recipe_id) VALUES (%s, %s)",
            ingredient_recipe_pairs,
        )


def init_db(csv_file: str):
    try:
        db_connection = get_db_connection()
        logging.info("Successfully connected to postgres.")
    except psycopg.OperationalError:
        logging.error("Failed to connect to postgres. Database initialisation failed.")
        return

    ingredient_id_map, recipe_id_map, ingredient_recipe_pairs = generate_table_values(
        csv_file
    )
    logging.info(f"Retrieved initial db values from {csv_file}")

    create_tables(
        db_connection, ingredient_id_map, recipe_id_map, ingredient_recipe_pairs
    )
    logging.info("Successfully initialised database.")


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)

    csv_file = os.environ["INIT_RECIPES_CSV"]
    init_db(csv_file)
