"""
DBConn class is used to talk to database with sql
Sample usage:
database = dbconn.DBConn()
table_1 = database.run_sql('SELECT * FROM user_accounts;')
"""

import os
import psycopg
from dotenv import load_dotenv


class DBConn:
    """
    DBConn class to create a connection pool and run SQL queries
    """

    def __init__(self) -> None:
        """
        Initialize connection pool with connection string or env
        create an optional cache storage
        """
        # Get the connection string from the environment variable
        load_dotenv()
        self.connection_string = os.getenv("DATABASE_URL")
        print("DEBUG")
        print(self.connection_string)

    def run_sql(self, sql_query: str) -> list:
        """
        Run SQL query on existing connection pool
        return empty list if no result or status is false
        does not update cache
        """
        # Get a connection from the pool
        conn = psycopg.connect(self.connection_string)
        # Create a cursor object
        cur = conn.cursor()
        # Execute SQL commands to retrieve the current time and version from PostgreSQL
        cur.execute(sql_query)
        results = cur.fetchall()
        # Close the cursor and return the connection to the pool
        cur.close()

        return results
