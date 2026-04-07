import sqlite3
import pandas as pd
from pathlib import Path

DANGEROUS_KEYWORDS = [
    'DROP', 'DELETE', 'UPDATE', 'INSERT', 'ALTER', 
    'TRUNCATE', 'REPLACE', 'CREATE', 'RENAME'
]

def execute_sqlite_query(sql):
    # Safety check - block any destructive SQL commands
    sql_upper = sql.upper()
    for keyword in DANGEROUS_KEYWORDS:
        if keyword in sql_upper:
            return "⚠️ Sorry, I can only retrieve data and cannot modify the database."

    # Path to your database
    current_dir = Path(__file__)
    root_dir = Path(__file__).parent
    db_path = f"{root_dir}/PropertyManagement.db"
    
    try:
        # Establish connection to SQLite
        conn = sqlite3.connect(db_path)
        
        # Execute query and return as DataFrame
        try:
            data_frame = pd.read_sql_query(sql, conn)
            return data_frame
        except Exception as qe:
            print("Query Error:", qe)
            return "Query compilation error - please try rephrasing your question"
            
    except Exception as e:
        print("Database Error:", e)
        return "Database connection error"
        
    finally:
        try:
            conn.close()
        except:
            pass

if __name__ == "__main__":
    # Test query
    query = "SELECT Property_Name, Pct_Occ FROM property_summary ORDER BY Pct_Occ DESC"
    print(execute_sqlite_query(query))