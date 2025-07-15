import sqlite3
import pandas as pd
from src.config import DB_PATH

def get_db_connection():
    """Creates and returns a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    return conn

def execute_sql_from_file(conn, sql_file):
    """Executes an SQL script from a file."""
    with open(sql_file, 'r') as f:
        sql_script = f.read()
    cursor = conn.cursor()
    cursor.executescript(sql_script)
    conn.commit()

def insert_data(conn, df, table_name):
    """Inserts data from a pandas DataFrame into a database table."""
    df.to_sql(table_name, conn, if_exists='append', index=False)
