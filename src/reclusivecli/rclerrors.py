#!/usr/bin/env python3


# Generic error for other errors to inherit
class GenericError(Exception):
    def __init__(self, number, error_type, cause, message):
        super().__init__()
        self.number = number    # int
        self.error_type = error_type    # string
        self.cause = cause  # depends
        self.message = message  # string

    def __dict__(self):
        return {
            "number": self.number,
            "error_type": self.error_type,
            "cause": self.cause,
            "message": self.message
        }


# CommandError: Unknown Flag
class Error101(GenericError):
    """
    The cause here is a list with two items: [unknown_flag_name, commmand]
    -   unknown_flag_name: the name of the flag that generates the error
    -   command: the command for which the flag was passed
    """

    def __init__(self, cause):
        error_type = "CommandError"
        number = 101

        super().__init__(
            number,
            error_type,
            cause,
            "%s%d: The flag %s is not a valid possibility for the command %s.\n" % (error_type, number, cause[0], cause[1])
        )


# CommandError: Unknown Flag
class Error102(GenericError):
    """
    The cause here is a list with two items: [unknown_flag_name, commmand]
    -   unknown_flag_name: the name of the flag that generates the error
    -   command: the command for which the flag was passed
    """

    def __init__(self, cause):
        error_type = "CommandError"
        number = 102

        super().__init__(
            number,
            error_type,
            cause,
            "%s%d: The flag %s is not a valid possibility for the command %s.\n" % (error_type, number, cause[0], cause[1])
        )


# CommandError: Unknown Subcommand
class Error103(GenericError):
    """
    The cause here is a list with two items: [unknown_subcommand_name, commmand]
    -   unknown_subcommand_name: the name of the subcommand that generates the error
    -   command: the command for which the subcommand was passed
    """

    def __init__(self, cause):
        error_type = "CommandError"
        number = 103

        super().__init__(
            number,
            error_type,
            cause,
            "%s%d: The subcommand %s is not a valid possibility for the command %s.\n" % (error_type, number, cause[0], cause[1])
        )


# CommandError: More Arguments Than Necessary
class Error104(GenericError):
    """
    The cause here is just a string with the name of the command that generated the error
    """

    def __init__(self, cause):
        error_type = "CommandError"
        number = 104

        super().__init__(
            number,
            error_type,
            cause,
            "%s%d: More Arguments than necessary were passed to the command %s.\n" % (error_type, number, cause)
        )


# CommandError: Less Arguments than necessary
class Error105(GenericError):
    """
    The cause here is just a string with the name of the command that generated the error
    """

    def __init__(self, cause):
        error_type = "CommandError"
        number = 105

        super().__init__(
            number,
            error_type,
            cause,
            "%s%d: Less Arguments than necessary were passed to the command %s.\n" % (error_type, number, cause)
        )


# FlagError: Less Arguments Than Necessary
class Error201(GenericError):
    """
    The cause here is just a string with the name of the flag that generated the error
    """

    def __init__(self, cause):
        error_type = "FlagError"
        number = 201

        super().__init__(
            number,
            error_type,
            cause,
            "%s%d: Less Arguments than necessary were passed to the flag %s.\n" % (error_type, number, cause)
        )


# StackError: Less Arguments Than Necessary
class Error301(GenericError):
    """
    The cause here is just a string with the name of the stack that generated the error
    """

    def __init__(self, cause):
        error_type = "StackError"
        number = 301

        super().__init__(
            number,
            error_type,
            cause,
            "%s%d: Less Arguments than necessary were passed to the stack %s.\n" % (error_type, number, cause)
        )


# StackError: Unknown Abbreviation
class Error302(GenericError):
    """
    The cause here is a list with two items: [abbreviation, stack]
    -   abbreviation: the char of the abbreviation that generates the error
    -   stack: the command for which the abbreviation was passed
    """

    def __init__(self, cause):
        error_type = "StackError"
        number = 302

        super().__init__(
            number,
            error_type,
            cause,
            "%s%d: The abbreviation %s inside the stack %s isn't valid for the current context.\n" % (error_type, number, cause[0], cause[1])
        )
