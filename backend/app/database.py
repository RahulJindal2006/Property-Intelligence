import sqlite3
import pandas as pd
from app.config import DB_PATH


def get_connection():
    return sqlite3.connect(DB_PATH)


def query_df(sql: str) -> pd.DataFrame:
    conn = get_connection()
    try:
        return pd.read_sql_query(sql, conn)
    finally:
        conn.close()
