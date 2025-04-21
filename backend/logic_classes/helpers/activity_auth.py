"""
authenticate the user and the activity
TO CHECK:
- if the user is authed
- if the user have access to the activity
- (if is_admin is set to true):
   - if the user is admin of the activity
"""

from backend.logic_classes.helpers import user_name_flatten as unf
from backend.flask_api import dbconn


def act_auth(
    database: dbconn.DBConn, args: dict, is_admin: bool = False
) -> tuple[int, list]:
    """
    Authenticate the user and the activity
    args: the entire args received from reqparse
    database: the database connection
    is_admin: if true, check if the user is admin of the activity
    Assumes: user is authed
    return:
        0: all good
        -1: certain required args not found
        2: activity not found
        3: user not allowed to see this activity
        4: user not admin of this activity but user can see this activity
    """
    required_args = ["uid", "reauth_jwt", "act_id"]
    for arg in required_args:
        if arg not in args or args[arg] is None:
            return -1, []
    query = "SELECT * FROM activity WHERE act_id = %s"
    table_1 = database.run_sql(query, (args["act_id"],))
    if not table_1:
        return 2, []
    # Check if the user is allowed to see this activity
    if args["uid"] not in unf.user_flatten(table_1[0]["uids"]):
        return 3, []
    # Check if the user is admin of this activity
    if is_admin and args["uid"] not in table_1[0]["admin_uids"]:
        return 4, table_1
    return 0, table_1
