import os

import backoff
import psycopg


@backoff.on_exception(backoff.constant, psycopg.OperationalError, max_tries=20)
def get_db_connection():
    return psycopg.connect(
        host=os.environ["POSTGRES_HOST"],
        dbname=os.environ["POSTGRES_DB"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
    )
