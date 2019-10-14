#!/usr/bin/env python3

import re
import sys
import json
import rclerrors
from rcllib import *

"""
    The Reclusive Programmer CLI lib, part of Reclusive Box Project
    TO-DO:
    -   Test if you need to turn abbreviations mandatory
"""


def command_to_dict(rcli_spec, arglist):
    spec = json.loads(rcli_spec)

    main_command = {
        "name": spec["name"],
        "flags": [],
        "subcommand": {},
        "args": []
    }

    current_index = 0

    while current_index < len(arglist) and need_args(spec, main_command):
        if is_valid_subcommand(arglist[current_index], spec):
            current_index = resolve_subcommand(get_subcommand(spec, arglist[current_index]), main_command, arglist, current_index)
        elif is_valid_stack(arglist[current_index], spec):
            current_index = resolve_stack(get_stack(spec, arglist[current_index]), main_command, arglist, current_index)
        elif is_valid_flag(arglist[current_index], spec):
            current_index = resolve_flag(get_flag(spec, arglist[current_index]), main_command, arglist, current_index)
        else:
            current_index = resolve_arg(spec, main_command, arglist, current_index)

    if not correct_arg_number(spec, main_command):
        raise rclerrors.Error105(main_command["name"])

    return main_command


if __name__ == "__main__":
    jsonstring = r'{"name":"main","args":-1,"flags":[{"name":"help","args":0,"abbreviation":"h"}],"subcommands":[{"name":"subcommand1","args":1,"flags":[{"name":"recursive","args":0}]}]}'
    commandstring = "main -h extracommand1 extracommand1"

    # try:
    print(json.dumps(command_to_dict(jsonstring, commandstring.split(" ")[1:])))
    # except rclerrors.GenericError as current_error:
    #     print(current_error.message)
