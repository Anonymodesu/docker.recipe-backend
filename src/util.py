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


def get_recipes():
    conn = get_db_connection()

    with conn, conn.cursor(row_factory=dict_row) as cur:
        cur.execute("SELECT name FROM recipes")
        records = [row["name"] for row in cur.fetchall()]

    return records
