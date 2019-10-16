#!/usr/bin/env python3

"""
Just some simple functions needed by rcli.
"""


import rclerrors
import re
import json


def correct_arg_number(spec, obj):
    if spec["args"] > 0:
        return spec["args"] == len(obj["args"])
    else:
        return (spec["args"] * -1) <= len(obj["args"])


def need_args(spec, obj):
    if spec["args"] < 0:
        return True
    else:
        return len(obj["args"]) < spec["args"]


def generate_flag_map(spec):
    to_return = {}
    try:
        for flag in spec["flags"]:
            to_return[flag["name"]] = flag
    finally:
        return to_return


def generate_compact_flag_map(spec):
    to_return = {}
    try:
        for flag in spec["flags"]:
            try:
                to_return[flag["abbreviation"]] = flag
            finally:
                pass
    finally:
        return to_return


def generate_subcommand_map(spec):
    to_return = {}
    try:
        for subcommand in spec["subcommands"]:
            to_return[subcommand["name"]] = subcommand
    finally:
        return to_return


def sanify_stack(stack):
    to_return = []

    for c in stack[1:]:
        if c not in to_return:
            to_return.append(c)

    return to_return


def get_subcommand(spec, name):
    try:
        return generate_subcommand_map(spec)[name]
    except KeyError:
        raise rclerrors.Error103([name, spec["name"]])


def get_flag(spec, name):
    if is_flag(name):
        try:
            return generate_flag_map(spec)[name[2:]]
        except KeyError:
            raise rclerrors.Error102([name, spec["name"]])

    elif is_compact_flag(name):
        try:
            return generate_compact_flag_map(spec)[name[1:]]
        except KeyError:
            raise rclerrors.Error102([name, spec["name"]])

    raise rclerrors.Error102([name, spec["name"]])


def get_stack(spec, name):
    to_return = []

    given = sanify_stack(name)
    flags = generate_compact_flag_map(spec)

    for letter in given:
        try:
            to_return.append(flags[letter])
        except KeyError:
            raise rclerrors.Error302([letter, name])

    return to_return


def is_arg(arg):
    if not (is_flag(arg) or is_stack(arg) or is_compact_flag(arg)):
        return True
    else:
        return False


def is_flag(arg):
    matches = re.findall(r'^--[A-Za-z]\S+$', arg)
    if len(matches) != 1:
        return False
    else:
        return True


def is_compact_flag(arg):
    matches = re.findall(r'^-[A-Za-z]$', arg)
    if len(matches) != 1:
        return False
    else:
        return True


def is_stack(arg):
    matches = re.findall(r'^-[A-Za-z][A-Za-z]+$', arg)
    if len(matches) != 1:
        return False
    else:
        return True


def is_subcommand(arg):
    matches = re.findall(r'^[A-Za-z]\S+$', arg)
    if len(matches) != 1:
        return False
    else:
        return True


def is_valid_flag(arg, spec):
    if is_flag(arg):
        if arg[2:] in generate_flag_map(spec).keys():
            return True
        else:
            return False
    elif is_compact_flag(arg):
        if arg[1:] in generate_compact_flag_map(spec).keys():
            return True
        else:
            return False
    else:
        return False


def is_valid_stack(arg, spec):
    if not is_stack(arg):
        return False

    given = set(re.findall(r'^-([A-Za-z][A-Za-z]+)$', arg)[0])
    possible = generate_compact_flag_map(spec).keys()
    for letter in given:
        if letter not in possible:
            return False
    return True


def is_valid_subcommand(arg, spec):
    if arg in generate_subcommand_map(spec).keys():
        return True
    else:
        return False


def resolve_subcommand(spec, obj, arglist, index):
    subcommand = {
        "name": spec["name"],
        "flags": [],
        "subcommand": {},
        "args": []
    }

    current_index = index + 1

    while current_index < len(arglist):
        if is_valid_subcommand(arglist[current_index], spec):
            current_index = resolve_subcommand(get_subcommand(spec, arglist[current_index]), subcommand, arglist, current_index)
        elif is_valid_stack(arglist[current_index], spec):
            current_index = resolve_stack(get_stack(spec, arglist[current_index]), subcommand, arglist, current_index)
        elif is_valid_flag(arglist[current_index], spec):
            current_index = resolve_flag(get_flag(spec, arglist[current_index]), subcommand, arglist, current_index)
        elif need_args(spec, subcommand):
            current_index = resolve_arg(spec, subcommand, arglist, current_index)
        else:
            current_index += 1

    if not correct_arg_number(spec, subcommand):
        raise rclerrors.Error105(subcommand["name"])

    obj["subcommand"] = subcommand
    # pdb.set_trace()
    return current_index


def resolve_stack(specs, obj, arglist, current_index):
    index_to_return = current_index + 1
    for spec in specs:
        index_to_return = resolve_flag(spec, obj, arglist, index_to_return - 1)

    return index_to_return


def resolve_flag(spec, obj, arglist, current_index):
    flag = {
        "name": spec["name"],
        "args": []
    }

    index_to_return = current_index + 1

    while need_args(spec, flag) and index_to_return < len(arglist):
        if is_arg(arglist[index_to_return]):
            index_to_return = resolve_arg(spec, flag, arglist, index_to_return)
        else:
            raise rclerrors.Error201(flag["name"])

    if not correct_arg_number(spec, flag):
        raise rclerrors.Error201(flag["name"])

    obj["flags"].append(flag)
    return index_to_return


def resolve_arg(spec, obj, arglist, current_index):
    index_to_return = current_index

    obj["args"].append(arglist[index_to_return])
    index_to_return += 1

    return index_to_return


if __name__ == "__main__":
    test_spec = r'{"name":"main","args":0,"flags":[{"name":"help","args":0,"abbreviation":"h"}],"subcommands":[{"name":"subcommand1","args":1,"flags":[{"name":"recursive","args":0}]}]}'

    dictspec = json.loads(test_spec)

    print(is_valid_subcommand("subcommand1", dictspec))
