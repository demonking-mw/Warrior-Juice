"""
Edit activity informations that are non-crit

NOTE: CREATION OF TASKS SHOULD ONLY BE DONE THROUG ACTIVITY CLASS
reason: Otherwise the user must enter a path to the task which is annoying
procedure: create empty task, go to tasks, modify them

Specific actions of this class:
- change due date
- change title
- change brief
- add/drop things in aux_info
- mod task tree

To mod task tree:
- provide the modified task tree (should also create empty tasks)
- provide a list of task ids to purge (should also purge tasks)
"""

from backend.flask_api import dbconn
from backend.logic_classes import user_auth


class ActInfoEdit:
    """
    Args:
    -

    Actions:
    - mod due date
    - mod act_title
    - mod act_brief
    - add/mod/drop items in aux_info
    - set task tree
    - purge task tree with a list of task ids
    """

    def __init__(self, database: dbconn.DBConn, args: dict = None) -> None:
        self.database = database
        self.args = args
        self.authed = False
        self.new_jwt = None
        auth_class = user_auth.UserAuth(database, args)
        self.auth_result, self.auth_code = auth_class.login_jwt()
        if self.auth_code == -1:
            print("ERROR:" + str(self.auth_result))
        if self.auth_result and self.auth_result["status"]:
            self.authed = True
