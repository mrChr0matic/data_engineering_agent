import sqlite3
from langchain.tools import tool

DB_PATH = "data/sql_store.db"

@tool 
def run_sql(query : str) -> str:
    """
    Execute a SQL query against the SQLite database and return the results.
    Use this tool whenever you need to retrieve or inspect data stored in the database.
    Input should be a valid SQL query string.
    """
    try:
        query = query.strip()
        if not query.lower().startswith("select"):
            return "Error: Only SELECT queries are allowed."
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute(query)
        rows = cursor.fetchall()
        
        conn.close()
        
        return str(rows)
    except Exception as e:
        return f"SQL Error : {str(e)}"