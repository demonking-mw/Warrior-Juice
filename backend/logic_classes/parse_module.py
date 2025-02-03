"""
parse the user input during a module creation and return the parsed data
Calculate and generate information to reduce user workload
"""

from dataclasses import dataclass
from flask_restful import reqparse


@dataclass
class ModuleData:
    """
    ModuleData class to store the data for a module
    """


class ParseModule:
    """
    ParseModule class to parse the user input and generate information
    """

    def __init__(self, args: dict) -> None:
        """
        Initialize the class with the user input
        args is actually reqparse.RequestParser().parse_args()
        However, treat it as a dictionary will work
        """
        self.args = args
        self.mod_info = self.reg_parse()

    def reg_parse(self) -> ModuleData:
        """
        Parse the user input for registration
        Use self.args
        """
        return ModuleData()

    def validate(self) -> bool:
        """
        Validate the user input
        Return True if the module is valid
        """
        return True

    def to_command(self) -> tuple[bool, str]:
        """
        Return a command that api.py can run to generate the module
        the boolean in front is whether the information is enough to generate the module
        """
        # return True, f"python3 -m {self.args['module']}"
