"""
Naming logic: 
classname_action

Commenting:
what for, what is required
"""

# pylint: disable=import-error
from flask_restful import reqparse

# User Auth
# Replacing Login and Regis
#######################################################################################
user_auth = reqparse.RequestParser()
user_auth.add_argument(
    "type",
    type=str,
    help="Type is required, can be eup or go or jwt or jwt_check",
    required=True,
)
user_auth.add_argument(
    "jwt_token", type=str, help="JWT token for go type", required=False, default=None
)
user_auth.add_argument(
    "reauth_jwt",
    type=str,
    help="JWT token provided from first login, good for 1h",
    required=False,
    default=None,
)
user_auth.add_argument("action", type=str, help="login/signup", required=False)
user_auth.add_argument("email", type=str, help="Email", required=False)
user_auth.add_argument("uid", type=str, help="User ID", required=False)
user_auth.add_argument("pwd", type=str, help="Password", required=False)
user_auth.add_argument("user_name", type=str, help="Name", required=False)
# If eup, action is also required
# if go, jwt_token is required

# modify user: username, pwd(not mandatory), new_pwd, email, tier, detail
user_modify = reqparse.RequestParser()
user_modify.add_argument(
    "auth_type",
    type=str,
    help="Account/auth type is required: eup/go/recover, auth is different for the two types",
    required=True,
)
user_modify.add_argument(
    "uid", type=str, help="UID is required, not changable", required=True
)
user_modify.add_argument(
    "action",
    type=str,
    help="Action is required, can be change or delete",
    required=True,
)
user_modify.add_argument(
    "jwt_token", type=str, help="JWT token for go type", required=False, default=None
)
user_modify.add_argument(
    "user_name", type=str, help="Existing user name", required=False
)
user_modify.add_argument("pwd", type=str, help="Old password, for auth", required=False)
user_modify.add_argument("new_pwd", type=str, help="New password", required=False)
user_modify.add_argument(
    "new_user_name", type=str, help="New user name", required=False
)
user_modify.add_argument(
    "auth_str", type=str, help="Auth string for password recovery", required=False
)
#######################################################################################

# User Info Edit Reqs
#######################################################################################
userinfo_get = reqparse.RequestParser()
userinfo_get.add_argument(
    "reauth_jwt",
    type=str,
    help="JWT token provided from first login, good for 1h",
    required=True,
    default=None,
)
userinfo_get.add_argument(
    "uid", type=str, help="User ID or sub for google oauth", required=True
)

userinfo_post = reqparse.RequestParser()
userinfo_post.add_argument(
    "reauth_jwt",
    type=str,
    help="JWT token provided from first login, good for 1h",
    required=True,
    default=None,
)
userinfo_post.add_argument(
    "uid", type=str, help="User ID or sub for google oauth", required=True
)
userinfo_post.add_argument(
    "act_ids",
    type=str,
    help="List of activity ids as string, split with comma only, no space",
    required=False,
    default="",
)
userinfo_post.add_argument(
    "sess_ids",
    type=str,
    help="List of session ids as string, split with comma only, no space",
    required=False,
    default="",
)

#######################################################################################

# Activity Reqs
#######################################################################################
# get activity: user_name(optional), activity_id(optional)
activity_get = reqparse.RequestParser()
activity_get.add_argument(
    "get_all",
    type=bool,
    help="Get all activities belonging to user? field required",
    required=True,
)
activity_get.add_argument(
    "user_name", type=str, help="User name is required", required=False
)
activity_get.add_argument("act_id", type=int, help="Activity id", required=False)


# activity creation: Mandatory: act_title, user name tree.
activity_create = reqparse.RequestParser()
activity_create.add_argument(
    "act_title", type=str, help="Activity title is required", required=True
)
activity_create.add_argument(
    "user_name", type=dict, help="User name tree is required", required=True
)
activity_create.add_argument(
    "admin_user_name", type=list, help="admin name list is required", required=True
)
activity_create.add_argument("act_type", type=str, help="Activity type", required=False)
activity_create.add_argument(
    "due_date",
    type=str,
    help="Due date in the form '2025-02-02 14:30:00'",
    required=False,
)
activity_create.add_argument(
    "act_brief", type=str, help="Activity brief, up to 256 char", required=False
)
activity_create.add_argument(
    "aux_info", type=dict, help="additional info for activity", required=False
)
activity_create.add_argument(
    "task_tree",
    type=dict,
    help="tree of all subtask ids, value for each entry being the title of the task",
    required=False,
)

activity_modify = reqparse.RequestParser()
activity_modify.add_argument(
    "action",
    type=str,
    help="Action is required, can be change or delete",
    required=True,
)
activity_modify.add_argument("act_id", type=int, help="Activity id", required=True)
activity_modify.add_argument(
    "user_name", type=str, help="user_name is required", required=True
)
activity_modify.add_argument(
    "act_type", type=str, help="type of activity", required=False
)
activity_modify.add_argument(
    "user_name_tree", type=dict, help="user_name_tree", required=False
)
activity_modify.add_argument(
    "admin_user_name", type=list, help="list of admin", required=False
)
activity_modify.add_argument(
    "due_date",
    type=str,
    help="Due date in the form '2025-02-02 14:30:00'",
    required=False,
)
activity_modify.add_argument(
    "act_title", type=str, help="activity title", required=False
)
activity_modify.add_argument(
    "act_brief", type=str, help="Activity brief, up to 256 char", required=False
)
activity_modify.add_argument(
    "aux_info", type=dict, help="additional info for activity", required=False
)
activity_modify.add_argument(
    "task_tree",
    type=dict,
    help="tree of all subtask ids, pre-defined slot uses -1",
    required=False,
)
