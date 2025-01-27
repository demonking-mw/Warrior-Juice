import dbconn

database = dbconn.DBConn()

database.run_sql(
    """INSERT INTO user_accounts VALUES(2, 'mw_0123', '4321', 'tier1', ARRAY[]::integer[], ARRAY[]::integer[], ARRAY[]::integer[])"""
)
table_2 = database.run_sql("SELECT * FROM user_accounts;")
print(table_2)
del database
