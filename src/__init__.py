#!/usr/bin/env python3

from reclusivecli.rcllib import resolve_subcommand

name = "reclusivecli"

"""
    The Reclusive Programmer CLI lib, part of Reclusive Box Project
    TO-DO:
    -   Test if you need to turn abbreviations mandatory
"""


def parse_command(reclusivecli_spec, arglist):

    main_command = {
        "subcommand": {}
    }

    resolve_subcommand(reclusivecli_spec, main_command, arglist, 0)

    return main_command["subcommand"]
