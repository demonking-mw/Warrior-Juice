"""
Naming logic: 
classname_action

Commenting:
what for, what is required
"""

# pylint: disable=import-error
from flask_restful import reqparse

# Activity Get
#######################################################################################
activity_get = reqparse.RequestParser()
activity_get.add_argument("uid", type=str, help="User ID is required", required=True)
activity_get.add_argument(
    "reauth_jwt",
    type=str,
    help="JWT token provided from first login, good for 1h",
    required=True,
    default=None,
)
activity_get.add_argument(
    "get_type",
    type=str,
    help="one for one act as is, all for all acts of a user, full for one act with tasks",
    required=True,
)
activity_get.add_argument(
    "act_id", type=int, help="Activity ID, required if get_all is False", required=False
)

#######################################################################################

#######################################################################################
# Activity Create
activity_create = reqparse.RequestParser()
activity_create.add_argument("uid", type=str, help="User ID is required", required=True)
activity_create.add_argument(
    "reauth_jwt",
    type=str,
    help="JWT token provided from first login, good for 1h",
    required=True,
    default=None,
)
activity_create.add_argument(
    "act_title", type=str, help="Activity title is required", required=True
)
# user name tree will be updated after
# admin user name will be updated after
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
    "act_type", type=str, help="type of activity", required=True
)
#######################################################################################

#######################################################################################
# Activity Modify
activity_crit_mod = reqparse.RequestParser()
activity_crit_mod.add_argument(
    "act_type",
    type=str,
    help="For changing act_type, not required",
    required=False,
)
activity_crit_mod.add_argument(
    "user_action",
    type=str,
    help="for modifying uids, can be put, add, purge, leave blank for no change",
    required=False,
)
activity_crit_mod.add_argument(
    "target_uid",
    type=str,
    help="the target uid to add or purge",
    required=False,
)
activity_crit_mod.add_argument(
    "uid_tree",
    type=dict,
    help="modified uid tree, directly from frontend",
    required=False,
)
activity_crit_mod.add_argument(
    "uid_path",
    type=str,
    help="path to insert uid, will create if not exist, optional, separate with /, no space around",
    required=False,
)
activity_crit_mod.add_argument(
    "admin_action",
    type=int,
    help="Action for admin, leave blank if no need. Target: add, remove",
    required=False,
)
# PURGE WILL ALSO HAVE TO REMOVE ACTIVITY FROM USER_ACCOUNTS.

# Activity Reqs
#######################################################################################

#######################################################################################
