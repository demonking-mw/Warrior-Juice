"""
Experimental backend with local db
run from backend:
python -m api_test.api_1
"""

from flask import Flask
from flask_restful import Api, Resource, reqparse
import psycopg
from . import dbconn


app = Flask(__name__)
api = Api(app)

# Requiring user_name and passowrd for login
user_req_args = reqparse.RequestParser()
user_req_args.add_argument(
    "user_name", type=str, help="User name is required", required=True
)
user_req_args.add_argument("pwd", type=str, help="Password is required", required=True)

# Requiring user_name, email, and password for registration
user_regis_args = reqparse.RequestParser()
user_regis_args.add_argument(
    "user_name", type=str, help="User name is required", required=True
)
user_regis_args.add_argument("email", type=str, help="Email is required", required=True)
user_regis_args.add_argument(
    "pwd", type=str, help="Password is required", required=True
)


class User(Resource):
    """
    dbconn pooling not used, very slow for now
    deals with users
    """

    def get(self):
        """
        gets the user details with username and password
        """
        args = user_req_args.parse_args()
        database = dbconn.DBConn()
        sql_query = (
            f"SELECT * FROM user_accounts WHERE user_name = '{args['user_name']}';"
        )
        print("DEBUG: ", sql_query)
        try:
            table_1 = database.run_sql(sql_query)
            print(table_1)
        except psycopg.errors.UndefinedColumn as e:
            return {"status": False, "detail": {"status": "user not found"}}, 400
        database.close()
        if table_1 and table_1[0]["pwd"] == args["pwd"]:
            return {"status": True, "detail": table_1[0]}, 200
        else:
            return {"status": False, "detail": {"status": "password incorrect"}}

    def post(self):
        """
        creates a new user with username, email, and password
        no email varification, add here in the future
        """
        args = user_regis_args.parse_args()
        database = dbconn.DBConn()
        sql_query = f"INSERT INTO user_accounts VALUES('{args['user_name']}', '{args["pwd"]}', '{args["email"]}', 'tier1', ARRAY[]::integer[], ARRAY[]::integer[], ARRAY[]::integer[])"
        try:
            database.run_sql(sql_query)
            database.close()
            return {"status": True, "detail": {"status": "user created"}}, 201
        except psycopg.errors.UniqueViolation as e:
            database.close()
            return {"status": False, "detail": {"status": "user already exists"}}, 200


api.add_resource(User, "/user")

if __name__ == "__main__":
    app.run(debug=True)
