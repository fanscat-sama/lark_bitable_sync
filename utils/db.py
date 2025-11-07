import pymysql

from contextlib import contextmanager
from config.settings import default_conn_settings

# Mariadb settings
@contextmanager
def get_db_cursor(db_name: str = 'default'):
    if db_name == 'default':
        conn_settings = default_conn_settings
    conn = None
    cursor = None
    try:
        conn = pymysql.connect(**conn_settings)
        cursor = conn.cursor()
        yield cursor
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()