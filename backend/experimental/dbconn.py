import os
from psycopg2 import pool

class DBConn():
    def __init__(self):
        self.connection_string = os.getenv('DATABASE_URL')
        self.connection_pool = pool.SimpleConnectionPool(
            1,  # Minimum number of connections in the pool
            10,  # Maximum number of connections in the pool
            self.connection_string
        )

    def status(self) -> bool:
        '''
        Check if the connection pool is empty
        '''
        if self.connection_pool:
            return True
        return False

    def run_sql(self, sql: str) -> list:
        '''
        Run SQL query on existing connection pool
        return empty list if no result or status is false
        '''
        if not self.status():
            print("DEBUG: connection pool is empty")
            return []
        connection = self.connection_pool.getconn()
        cursor = connection.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        self.connection_pool.putconn(connection)
        return result
        