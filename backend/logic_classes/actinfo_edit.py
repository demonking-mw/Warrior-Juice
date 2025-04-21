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

import json

from datetime import datetime

from backend.flask_api import dbconn
from backend.logic_classes import user_auth
from backend.logic_classes.helpers import user_name_flatten as unf
from backend.logic_classes.helpers import activity_auth as act_auth
from backend.logic_classes.helpers import batch_ins_gen as big


class ActInfoEdit:
    """
    Args:
    -

    Actions:
    - mod due date (simple)
    - mod act_title (simple)
    - mod act_brief (simple)
    - mod aux_info (simple)(provide the modified aux_info dict)(ideally used by backend)
    - set task tree
    - purge task tree with a list of task ids

    REQUIRES: task_create_empty and task_delete function inserted in tasks_tree_set

    Calling order: ActInfoEdit(database, args), then edit()
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
        self.act_auth_result, self.act_table = act_auth.act_auth(
            self.database, self.args
        )
        self.to_modify = {}
        self.modded = self.apply_actions_simple()
        if self.tasks_tree_set():
            self.modded.append("tasks_tree")
        # self.to_modify is a dict storing which entry to modify
        # and what to modify it to

    def check_auth(self) -> bool:
        """
        Check if the user is authenticated
        """
        if not self.authed or self.act_auth_result != 0:
            print("DEBUG: auth failed or act_auth failed")
            return False
        return True

    def apply_actions_simple(self) -> list:
        """
        Apply simple actions to the activity
        - change due date
        - change act_title
        - change act_brief
        Return: a list of what entries were modified
        """
        if not self.check_auth():
            return []
        # Check if the user is allowed to see this activity
        moded = []
        if self.args["act_title"]:
            self.to_modify["act_title"] = self.args["act_title"]
            moded.append("act_title")
        if self.args["due_date"]:
            dd_formated = datetime.strptime(self.args["due_date"], "%Y-%m-%d %H:%M:%S")
            self.to_modify["due_date"] = dd_formated
            moded.append("due_date")
        if self.args["act_brief"]:
            self.to_modify["act_brief"] = self.args["act_brief"]
            moded.append("act_brief")
        if self.args["aux_info"]:
            self.to_modify["aux_info"] = self.args["aux_info"]
            moded.append("aux_info")
        return moded

    def tasks_tree_set(self) -> bool:
        """
        Set the task tree for the activity
        Requires a list of task ids to set
        Requires a task_create_empty function/codeblock, NOT IMPLEMENTED YET
        Requires a task_delete function/codeblock, NOT IMPLEMENTED YET
        For the above functions, input is the task id
        """
        if not self.check_auth():
            return False
        if not self.args["tasks_tree"]:
            return False
        # The user want to modify the task tree at this point
        # Stores the old tree for diff
        old_list = unf.user_flatten(self.act_table[0]["tasks_tree"])
        # task tree is basically user tree
        self.to_modify["tasks_tree"] = json.dumps(self.args["tasks_tree"])
        new_list = unf.user_flatten(self.args["tasks_tree"])
        for task in new_list:
            if task not in old_list:
                # task_create_empty(task), NOT IMPLEMENTED
                print("DEBUG: task_create_empty")
                print(task)
        if self.args["purge_tree"]:
            for task in old_list:
                if task not in new_list:
                    # task_delete(task), NOT IMPLEMENTED
                    print("DEBUG: task_delete")
                    print(task)
        return True

    def edit(self) -> tuple[dict, int]:
        """
        Edit the set stuff
        (basically performing what was told)
        Must be used AFTER modifying the to_modify dict using other funcitons
        """
        if not self.authed:
            return {"status": False, "detail": "User not authenticated"}, 401
        if self.act_auth_result != 0:
            return {"status": False, "detail": "Activity auth failed"}, 403
        if not self.to_modify:
            return {"status": False, "detail": "Nothing modified"}, -1
            # Should not happen through user input
        upd_query, values = big.create_query(
            "activity",
            self.to_modify,
            "act_id",
            self.args["act_id"],
        )
        self.database.run_sql(upd_query, values)
        return {
            "status": True,
            "detail": self.modded,
            "jwt": self.auth_result["jwt"],
        }, 200
