"""
create a squ query to update a list of items in a table given all the possible items

directly use the args dict from reqparse
"""


def create_query(
    table: str, params: dict, where_clause: str, where_value: any
) -> tuple[str, tuple]:
    """
    table is the name of the table
    params is a dict: name: value
    where_clause is the clause after where
    where_value is the value to be used in the where clause
    should be inserted at the end of the values tuple

    Example:
    from backend.logic_classes.helpers import batch_ins_gen as big
    targ_dict = {
        "user_sess_id": target_list,
    }
    upd_query, values = big.create_query(
        "user_accounts",
        targ_dict,
        "uid",
        self.args["uid"],
    )
    self.database.run_sql(upd_query, values)

    """
    set_clause = ", ".join([f"{key} = %s" for key in params.keys()])
    query = f"UPDATE {table} SET {set_clause} WHERE {where_clause} = %s"
    values = tuple(params[key] for key in params.keys()) + (where_value,)
    return query, values
