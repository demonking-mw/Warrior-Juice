''' 
A cool testing module for targeting dbconn.py

Test to varify the functionality of the functions in dbconn.py;
As documentation describes, following features should work: 
    database = dbconn.DBConn(file_cache=____)
    table_1 = database.run_sql('SELECT * FROM user_accounts;')
    del database
Test relies on mock database connection

'''

import unittest
import dbconn



'''
Case
Input:
Output:
Methodology

'''