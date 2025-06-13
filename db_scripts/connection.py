import sqlite3
def get_connection(db_path):
        with sqlite3.connect(db_path) as conn:
            return conn
