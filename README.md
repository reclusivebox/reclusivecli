# RCLI - The Reclusive Command Line Interface Library



This is just a small lib to help your programs to interpret command line arguments effortlessly.

# RCLI Rules

## Definitions

There are some rules to define a valid RCLI specification. First of all let's establish some definitions:

### Command

Commands are the main piece of a cli interface, there are possibly 2 types of commands: the main command and the subcommands. The main command is essentially the name of your program (ex: git, firefox), the sub commands are things you add to your specification to direct the user to certain parts of the program (ex: apt **install**, git **commit**).

Commands must:

- Start with a letter (A-Z, a-z)
- Say how many arguments they expect
- Say which flags are valid if any
- Say which subcommands are valid if any

### Flags

Flags are options that con change the default behavior of your program, flags may take arguments if they indicate it in the specification (ex: rm **--recursive**, rm **-r**). Flags can also have abbreviations that can be stacked.

Flags must:

- Start with two dashes ( **--** ) when passed to a command (ex: --recursive)
- Have a finite number of arguments if any

Flags can't:

- Receive other flags, as soon as other flag starts the current ends.

### Abbreviations

Compact ways to pass single flags to commands.

Abbreviations must:

- Start with a single dash ( **-** ) when passed to a command (ex: rm **-r**)
- Be represented by a single letter in the specification

Is a good practice to abbreviate flags that takes arguments with capital letters and the others with lower letters.  

### Stacks

Stacks are just a way to pass a lot of flags to a command in a simple way.

Stacks must:

- Start with a single dash ( **-** ) when passed to a command (ex: ls **-alt**)
- Be immediately followed by the necessary number of arguments if the stacked flags required any

## Writing the specification

The RCLI 1.0 specification is just a json that describes the cli of your program. To write a good specification you just need to know how to write flags and commands, things like stacks are handled by the RCLI interpreter.

### Flags

A json flag specification takes in three possible attributes:

- `"name"`: Just a string with the full name of the flag.
- `"args"`: A positive integer with how many arguments the flag can take (zero can also be passed here).
- `"abbreviation"`(OPTIONAL): A single character to represent this flag in compact mode and stacks.

Example:

```json
{
    "name": "recursive",
    "args": 0,
    "abbreviation": "r"
}
```

> You don't need to write the dashes (`-`) and the double dashes (`--`) for flags in the specification, only when using the command.

> Don't repeat abbreviations for flags, or only the first will work

### Commands

A json command specification takes in four possible attributes:

- "name": Just a string with the name of the command.
- `"args"`: A integer with the number of arguments the command can take, if zero is passed the command can receive unlimited number of arguments. If a negative is passed ex: -1, than the interpreter will see this as you saying that the program needs at least this amount, in this case, at least one argument.
- `"flags"`(OPTIONAL): A array with flags objects as explained in the previous section. This will indicate to the interpreter which flags are valid for the command.
- `"subcommands"`(OPTIONAL): A array with other command objects to be used as subcommands. This will indicate to the interpreter which subcommands are valid for the command.

Example:

```json
{
    "name": "cp",
    "args": -2,
    "flags": [
        {
            "name": "recursive",
            "args": 0,
            "abbreviation": "r"
        }
    ]
}
```

