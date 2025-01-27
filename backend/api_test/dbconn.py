"""
DBConn class is used to talk to database with sql
Sample usage:
database = dbconn.DBConn(file_cache=____)
table_1 = database.run_sql('SELECT * FROM user_accounts;')
del database
"""

import os
import psycopg
from psycopg_pool import ConnectionPool
from dotenv import load_dotenv


class DBConn:
    """
    DBConn class to create a connection pool and run SQL queries
    The cache option is good when you need to repeatedly access the same table
    Use del to clear cache
    """

    def __init__(self) -> None:
        """
        Initialize connection pool with connection string or env
        create an optional cache storage
        """
        # Get the connection string from the environment variable
        load_dotenv()
        self.connection_string = os.getenv("DATABASE_URL")
        self.conn_pool = ConnectionPool(self.connection_string)

    def run_sql(self, sql_query: str) -> list:
        """
        Run SQL query on existing connection pool
        return empty list if no result or status is false
        does not update cache
        """
        with self.conn_pool.connection() as conn:
            with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
                cur.execute(sql_query)
                results = []
                if cur.description is not None:
                    results = cur.fetchall()
                else:
                    conn.commit()

        return results
