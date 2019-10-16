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
        "subcommands": []
    }

    resolve_subcommand(spec, main_command, arglist, 0)

    return main_command["subcommands"][0]


if __name__ == "__main__":
    jsonstring = r'{"name":"main","args":-1,"flags":[{"name":"help","args":0,"abbreviation":"h"}],"subcommands":[{"name":"subcommand1","args":1,"flags":[{"name":"recursive","args":0}]}]}'
    commandstring = "main -h extracommand1 extracommand1"

    # try:
    print(json.dumps(command_to_dict(jsonstring, commandstring.split(" "))))
    # except rclerrors.GenericError as current_error:
    #     print(current_error.message)
