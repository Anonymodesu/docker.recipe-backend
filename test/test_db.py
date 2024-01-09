import os

import backoff
from psycopg.errors import UndefinedTable
from psycopg.rows import dict_row
import pytest
import requests
import requests.exceptions

from src.init_db import get_db_connection


@backoff.on_exception(backoff.constant, requests.exceptions.ConnectionError, max_tries=10)
def wait_for_webserver():
    response = requests.get("http://webserver/health").text
    assert response == "OK"


@backoff.on_exception(backoff.constant, UndefinedTable, max_tries=10)
def wait_for_database():
    conn = conn = get_db_connection(
        os.environ["POSTGRES_HOST"],
        os.environ["POSTGRES_DB"],
        os.environ["POSTGRES_USER"],
        os.environ["POSTGRES_PASSWORD"],
    )
    with conn, conn.cursor(row_factory=dict_row) as cur:
        cur.execute("SELECT count(*) AS count FROM ingredient_recipe_map")
        assert cur.fetchone()["count"] > 1


@pytest.fixture(scope="session")
def wait_for_services():
    wait_for_database()
    wait_for_webserver()


def test_foo(wait_for_services):
    pass