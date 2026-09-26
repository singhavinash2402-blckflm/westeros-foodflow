import os
import pyodbc


def get_connection():
    # Do not hard-code credentials or connection strings in Git.
    # Example:
    # set FOODFLOW_SQL_CONNECTION_STRING=Driver={ODBC Driver 18 for SQL Server};Server=...;Database=...;Uid=...;Pwd=...;Encrypt=yes;TrustServerCertificate=no;
    conn_str = os.getenv("FOODFLOW_SQL_CONNECTION_STRING")
    if not conn_str:
        raise RuntimeError(
            "FOODFLOW_SQL_CONNECTION_STRING is not set. "
            "Keep Azure SQL credentials outside the repository."
        )
    return pyodbc.connect(conn_str)


def insert_rows(cursor, sql, rows):
    if not rows:
        return
    cursor.fast_executemany = True
    cursor.executemany(sql, rows)


def fetch_map(cursor, sql, params=()):
    cursor.execute(sql, params)
    return {row[1]: row[0] for row in cursor.fetchall()}
