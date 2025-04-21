"""
parse a list of arguments and put them into columns, values, and params
"""


def qparser(targets: list, args: dict) -> tuple[list, list, list]:
    """
    Parse a list of arguments and put them into columns, values, and params
    Return: success count, columns, values, params
    """
    columns = []
    values = []
    params = []
    for target in targets:
        if args.get(target):
            columns.append(target)
            values.append("%s")
            params.append(args.get(target))
    return columns, values, params
