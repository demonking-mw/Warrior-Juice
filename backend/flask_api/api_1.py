"""
Experimental backend with local db
run from backend:
python -m api_test.api_1
"""

# pylint: disable=import-error
from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from .classes.user import User
from .classes.userinfo import UserInfo
from .classes.activity import Activity


app = Flask(__name__)
CORS(
    app,
    resources={r"/*": {"origins": "http://localhost:3000"}},
    supports_credentials=True,
)
api = Api(app)


@app.after_request
def apply_cors_headers(response):
    """Automatically add CORS headers to all responses"""
    response.headers["Access-Control-Allow-Origin"] = "http://localhost:3000"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS, PUT, DELETE"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response


api.add_resource(User, "/user")
api.add_resource(UserInfo, "/user/info")
api.add_resource(Activity, "/activity")

if __name__ == "__main__":
    app.run(debug=True)
