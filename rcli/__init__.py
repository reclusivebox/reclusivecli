#!/usr/bin/env python3

import re
import sys
import json
import rclerrors
from rcllib import resolve_subcommand

name = "rcli"

"""
    The Reclusive Programmer CLI lib, part of Reclusive Box Project
    TO-DO:
    -   Test if you need to turn abbreviations mandatory
"""


def command_to_dict(rcli_spec, arglist):
    spec = json.loads(rcli_spec)

    main_command = {
        "subcommand": {}
    }

    resolve_subcommand(spec, main_command, arglist, 0)

    return main_command["subcommand"]


# if __name__ == "__main__":
#     with open("test.json", "r") as jsonfile:
#         test_dict = json.loads(jsonfile.read())
#
#     for command in test_dict:
#         print(command_to_dict(json.dumps(test_dict[command]), command.split(" ")))
