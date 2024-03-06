import psycopg2
from functools import wraps
from dotenv import load_dotenv
import os

load_dotenv()


def db_connection(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        conn = None
        try:
            conn = psycopg2.connect(
                dbname=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                host=os.getenv("DB_HOST"),
                port=os.getenv("DB_PORT"),
            )
            cur = conn.cursor()

            result = func(cur, *args, **kwargs)

            conn.commit()
            return result
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

    return wrapper
