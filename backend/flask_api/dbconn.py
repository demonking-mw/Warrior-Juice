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
from psycopg.errors import QueryCanceled, OperationalError


class DBConn:
    """
    DBConn class to create a connection pool and run SQL queries
    The cache option is good when you need to repeatedly access the same table
    Use del to clear cache
    """

    # a connection pool is a method of connecting the application to an existing database
    # there are several benefits to a connection pool: security (so that user don't overwhelm the database)
    # I mean... what other ways are there? 

    def __init__(self) -> None:
        """
        Initialize connection pool with connection string or env
        create an optional cache storage
        """
        
        # connection string is a string that contains: things such as name, user, password, host, port
        # this this way we tell program which database it connects to
        # Xena was here
        # environmental variable is a variable we can access by the program; it is stored in a computer
        # thus it will not run into scope issues (DO NOT STORE THE ACCESSED ENVIRONMENTAL VARIABLE as global variable)
        # this is opposite to the purpose of environmental variable. The purpose of environmental variable is security
        # where global variable may need to be passed around and changed, making it hard to make sure every aspect of the
        # process is secure; using environmental variables we just need to ensure that the process of taking the 
        # variable is secure and the site of using the variable is secure 

        # technically the .env file is not much different than .txt file that store sensitive information
        # but it is a good convention and in case we want to store them as environmental variables
        # I feel like the below documentation is wrong: shouldn't load_dotenv() get information from .env to local
        # environmental variable?
        # we must be careful with the load_dotenv() function because it technically takes all the environmental
        # variables from the .env file 🙄. You know, you might want to take out unneccarry information. 

        # Get the connection string from the environment variable 
        load_dotenv()
        self.connection_string = os.getenv("DATABASE_URL")
        self.conn_pool = ConnectionPool(
            self.connection_string, kwargs={"sslmode": "require"}
        )

    def run_sql(self, sql_query: str, params=None) -> list:
        """
        Run SQL query on existing connection pool
        return empty list if no result or status is false
        does not update cache
        """
        try:
            with self.conn_pool.connection() as conn:
                with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
                    cur.execute(sql_query, params)
                    results = []
                    if cur.description is not None:
                        results = cur.fetchall()
                    else:
                        conn.commit()
        except (QueryCanceled, OperationalError) as e:
            print(f"Database error: {e}")
            results = []
        return results

    def close(self) -> None:
        """
        Close all connections in the pool
        """
        self.conn_pool.close()
