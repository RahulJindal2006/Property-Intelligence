import sqlite3
import pandas as pd
from app.config import DB_PATH

DANGEROUS_KEYWORDS = [
    'DROP', 'DELETE', 'UPDATE', 'INSERT', 'ALTER',
    'TRUNCATE', 'REPLACE', 'CREATE', 'RENAME'
]


def execute_sqlite_query(sql: str):
    sql_upper = sql.upper()
    for keyword in DANGEROUS_KEYWORDS:
        if keyword in sql_upper:
            return "Sorry, I can only retrieve data and cannot modify the database."

    try:
        conn = sqlite3.connect(DB_PATH)
        try:
            data_frame = pd.read_sql_query(sql, conn)
            return data_frame
        except Exception as qe:
            print("Query Error:", qe)
            return "Query compilation error - please try rephrasing your question"
        finally:
            conn.close()
    except Exception as e:
        print("Database Error:", e)
        return "Database connection error"
