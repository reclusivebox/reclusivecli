# ReclusiveCLI - The Reclusive Command Line Interpreter

This is just a small lib to help your programs to interpret command line arguments effortlessly.

1. [Installation](#installation)
2. [Usage](#usage)
3. [ReclusiveCLI Rules](#reclusivecli-rules)
   1. [Definitions](#definitions)
      1. [Command](#command-definition)
      2. [Flags](#flag-definition)
      3. [Abbreviation](#abbreviation-definition)
      4. [Stack](#stack-definition)
   2. [Writing the Specification](#writing-specs)
      1. [Flags](#flag-spec)
      2. [Commands](#command-spec)

# Installation <a name="installation"></a>

ReclusiveCLI was designed with python3 in mind. To install the latest version, please run:

```bash
pip install reclusivecli
```

You can also try the a specific version:

```bash
pip install git+https://github.com/reclusivebox/reclusivecli@alpha1
```

# Usage <a name="usage"></a>

```python
import reclusivecli
import sys
import json

args = sys.argv
with open("my_program_description.json", "r") as json_file:
    specification = json.loads(jsonfile.read())

useful_information = reclusivecli.parse_command(specification, args)
```

- I don't know how you want to receive your command's arguments, in this example I used  the `sys` module.
- The specification is a python `dict` describing the behavior of the program. Here I used json to write my specification, but you can use any language you want like YAML or XML as long as it can be loaded as a python `dict`.
- The `parse_command` function returns a python dict with the useful and formatted information for your program. To know more about the structure of this dict take a look at [here](#return-dict).

# ReclusiveCLI Rules <a name="reclusivecli-rules"></a>

## Definitions <a name="definitions"></a>

There are some rules to define a valid ReclusiveCLI specification. First of all let's establish some definitions:

### Command <a name="command-definition"></a>

Commands are the main piece of a cli interface, there are possibly 2 types of commands: the main command and the subcommands. The main command is essentially the name of your program (ex: git, firefox), the sub commands are things you add to your specification to direct the user to certain parts of the program (ex: apt **install**, git **commit**).

Commands must:

- Start with a letter (A-Z, a-z)
- Say how many arguments they expect
- Say which flags are valid if any
- Say which subcommands are valid if any
- Only take one subcommand per time if any

### Flags <a name="flag-definition"></a>

Flags are options that can change the default behavior of your program (ex: rm **--recursive**, rm **-r**), flags may take arguments if they indicate it in the specification. Flags can also have abbreviations that can be stacked (ex: ls **-alt**).

Flags must:

- Start with two dashes ( **--** ) when passed to a command in full form (ex: --recursive)
- Have a finite number of arguments if any

Flags can't:

- Receive other flags, as soon as other flag starts the current ends.

### Abbreviations <a name="abbreviation-definition"></a>

Compact ways to pass single flags to commands.

Abbreviations must:

- Start with a single dash ( **-** ) when passed to a command (ex: rm **-r**)
- Be represented by a single letter in the specification

> Is a good practice to abbreviate flags that takes arguments with capital letters and the others with lower letters.  
>

### Stacks <a name="stack-definition"></a>

Stacks are just a way to pass a lot of flags to a command in a simple way.

Stacks must:

- Start with a single dash ( **-** ) when passed to a command (ex: ls **-alt**)
- Be immediately followed by the necessary number of arguments if the stacked flags require any

## Writing the specification <a name="writing-specs"></a>

The ReclusiveCLI 1.0 specification is just a map that describes the cli of your program. To write a good specification you just need to know how to write flags and commands, things like stacks are handled by the RCL Interpreter.

### Flags <a name="flag-spec"></a>

A flag specification takes in three possible attributes:

- `"name"`: Just a string with the full name of the flag.
- `"args"`: A positive integer with how many arguments the flag can take (zero can also be passed here).
- `"abbreviation"`(OPTIONAL): A single character to represent this flag in compact mode and stacks.

Example:

```json
{	// json example
    "name": "recursive",
    "args": 0,
    "abbreviation": "r"
}
```

```yaml
# yaml example
name: "recursive"
args: 0
abbreviation: 'r'
```

> You don't need to write the dashes (`-`) and the double dashes (`--`) for flags in the specification, only when using the command.

> Don't repeat abbreviations for flags, or only the first will work

### Commands <a name="command-spec"></a>

A command specification takes in four possible attributes:

- `"name"`: Just a string with the name of the command.
- `"args"`: A integer with the number of arguments the command can take, if zero is passed the command don't process arguments. If a negative is passed ex: -1, than the interpreter will see this as you saying that the program needs at least this amount, in this case, at least one argument, but there's no upper limit.
- `"flags"`(OPTIONAL): An array with flags objects as explained in the previous section. This will indicate to the interpreter which flags are valid for the command.
- `"subcommands"`(OPTIONAL): An array with other command objects to be used as subcommands. This will indicate to the interpreter which subcommands are valid for the command.

> Remember: if you use a negative `arg` number with a subcommand it won't come back to reevaluate the main command, all the arguments after the subcommand will be passed to it, unless there's other subcommand.

Examples:

```json
{	// json example
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

```yaml
# yaml example
name: "cp"
args: -2
flags:
  -
    name: "recursive"
    args: 0
    abbreviation: 'r'
```

## What ReclusiveCLI gives me? <a name="return-dict"></a>

The return value of the `parse_command` function is very similar to the specification you give to the interpreter, the only differences are:

- The "args" attribute here isn't a integer but a list of strings with the arguments passed to the command or flag.
- There's no abbreviations here, the interpreter already solved them for you.
- There's no "subcommands" here, just "subcommand", a single command object.
- The flags here is a `dict` not a list, and each flag just contains a list with the args.

Examples for `git push origin master`:

```json
{	// json example
    "name": "git",
    "flags": [],
    "args": [],
    "subcommand":{
            "name": "push",
            "flags": {},
            "args": ["origin", "master"],
            "subcommand": {}
      }
}
```

```yaml
# yaml example
name: "git"
flags: []
args: []
subcommand:
  name: "commit"
  flags:
  	message: ["Your Message"]
  args: []
  subcommand: {}
```

Remember the `parse_command` function only gives you a python `dict`, the examples above were only to show what's gonna be inside this `dict`.
