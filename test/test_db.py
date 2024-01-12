import os

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


def test_foo(wait_for_services):
    pass
