#!/usr/bin/env python3

"""
Just some simple functions needed by reclusivecli.
"""


import reclusivecli.rclerrors
import re
import json


def correct_arg_number(spec, obj):
    """
        Takes in the specification for a object and the object itself and tells you if the object have enough arguments.
        This function is used when the object is ready to assure that nothing is missing.
    """

    if spec["args"] > 0:
        return spec["args"] == len(obj["args"])
    else:
        return (spec["args"] * -1) <= len(obj["args"])


def need_args(spec, obj):
    """
        Tells you if a object can still receive arguments.
        Used while the object isn't finished yet.
    """

    if spec["args"] < 0:
        return True
    else:
        return len(obj["args"]) < spec["args"]


def generate_flag_map(spec):
    """
        Just generate a simple map to acess the possible flags of a spec more easily.
    """

    to_return = {}
    try:
        for flag in spec["flags"]:
            to_return[flag["name"]] = flag
    finally:
        return to_return


def generate_compact_flag_map(spec):
    """
        Maps all the abbreviations of a spec to appropriate flags.
    """

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
    """
        Maps every subcommand name to a proper subcommand object.
    """

    to_return = {}
    try:
        for subcommand in spec["subcommands"]:
            to_return[subcommand["name"]] = subcommand
    finally:
        return to_return


def sanify_stack(stack):
    """
        Split the stack into a list of characters representing the flags
    """

    to_return = []

    for c in stack[1:]:
        if c not in to_return:
            to_return.append(c)

    return to_return


def get_subcommand(spec, name):
    """
        Returns a specific command object when given the appropriate command name.
    """

    try:
        return generate_subcommand_map(spec)[name]
    except KeyError:
        raise reclusivecli.rclerrors.Error103([name, spec["name"]])


def get_flag(spec, name):
    """
        Given a flag name or abbreviation, returns the flag object
    """

    if is_flag(name):
        try:
            return generate_flag_map(spec)[name[2:]]
        except KeyError:
            raise reclusivecli.rclerrors.Error102([name, spec["name"]])

    elif is_compact_flag(name):
        try:
            return generate_compact_flag_map(spec)[name[1:]]
        except KeyError:
            raise reclusivecli.rclerrors.Error102([name, spec["name"]])

    raise reclusivecli.rclerrors.Error102([name, spec["name"]])


def get_stack(spec, name):
    """
        Returns a map with each flag pecs for each flag inside a stack.
    """

    to_return = []

    given = sanify_stack(name)
    flags = generate_compact_flag_map(spec)

    for letter in given:
        try:
            to_return.append(flags[letter])
        except KeyError:
            raise reclusivecli.rclerrors.Error302([letter, name])

    return to_return


def is_arg(arg):
    """
        Tells you if something COULD be a argument for a command
    """

    if not (is_flag(arg) or is_stack(arg) or is_compact_flag(arg)):
        return True
    else:
        return False


def is_flag(arg):
    """
        Tells you if something COULD be a flag
    """

    matches = re.findall(r'^--[A-Za-z]\S+$', arg)
    if len(matches) != 1:
        return False
    else:
        return True


def is_compact_flag(arg):
    """
        Tells you if something COULD be a abbreviation
    """

    matches = re.findall(r'^-[A-Za-z]$', arg)
    if len(matches) != 1:
        return False
    else:
        return True


def is_stack(arg):
    """
        Tells you if something COULD be a stack
    """

    matches = re.findall(r'^-[A-Za-z][A-Za-z]+$', arg)
    if len(matches) != 1:
        return False
    else:
        return True


def is_subcommand(arg):
    """
        Tells you if something COULD be a subcommand
    """

    matches = re.findall(r'^[A-Za-z]\S+$', arg)
    if len(matches) != 1:
        return False
    else:
        return True


def is_valid_flag(arg, spec):
    """
        Tells you if something is a valid flag for a given spec
    """

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
    """
        Tells you if something is a valid stack for a given spec.
    """

    if not is_stack(arg):
        return False

    given = sanify_stack(arg)
    possible = generate_compact_flag_map(spec).keys()

    for letter in given:
        if letter not in possible:
            return False
    return True


def is_valid_subcommand(arg, spec):
    """
        Tells you if something is a valid subcommand for a given spec.
    """

    if arg in generate_subcommand_map(spec).keys():
        return True
    else:
        return False


def resolve_subcommand(spec, obj, arglist, index):
    """
        Given:
            - A ReclusiveCLI spec
            - A object under construction
            - A list of arguments
            - A index
        This function parses the comand in the index of the arglist. Putting it inside the object under construction. and returning the index the outside parser should focus on.
    """

    subcommand = {
        "name": spec["name"],
        "flags": {},
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
        raise reclusivecli.rclerrors.Error105(subcommand["name"])

    obj["subcommand"] = subcommand
    # pdb.set_trace()
    return current_index


def resolve_stack(specs, obj, arglist, current_index):
    """
        Given:
            - A ReclusiveCLI spec
            - A object under construction
            - A list of arguments
            - A index
        This function parses the stack in the index of the arglist. Putting it inside the object under construction. and returning the index the outside parser should focus on.
    """

    index_to_return = current_index + 1
    for spec in specs:
        index_to_return = resolve_flag(spec, obj, arglist, index_to_return - 1)

    return index_to_return


def resolve_flag(spec, obj, arglist, current_index):
    """
        Given:
            - A ReclusiveCLI spec
            - A object under construction
            - A list of arguments
            - A index
        This function parses the flag in the index of the arglist. Putting it inside the object under construction. and returning the index the outside parser should focus on.
    """

    flagname = spec["name"]
    flag = {
        "args": []
    }

    index_to_return = current_index + 1

    while need_args(spec, flag) and index_to_return < len(arglist):
        if is_arg(arglist[index_to_return]):
            index_to_return = resolve_arg(spec, flag, arglist, index_to_return)
        else:
            raise reclusivecli.rclerrors.Error201(flagname)

    if not correct_arg_number(spec, flag):
        raise reclusivecli.rclerrors.Error201(flagname)

    obj["flags"][flagname] = flag
    return index_to_return


def resolve_arg(spec, obj, arglist, current_index):
    """
        Given:
            - A ReclusiveCLI spec
            - A object under construction
            - A list of arguments
            - A index
        This function parses the argument in the index of the arglist. Putting it inside the object under construction. and returning the index the outside parser should focus on.
    """

    index_to_return = current_index

    obj["args"].append(arglist[index_to_return])
    index_to_return += 1

    return index_to_return


if __name__ == "__main__":
    test_spec = r'{"name":"main","args":0,"flags":[{"name":"help","args":0,"abbreviation":"h"}],"subcommands":[{"name":"subcommand1","args":1,"flags":[{"name":"recursive","args":0}]}]}'

    dictspec = json.loads(test_spec)

    print(is_valid_subcommand("subcommand1", dictspec))
