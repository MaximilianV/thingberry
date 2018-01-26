import re
from enum import Enum

def ask_yes_no_question(question):
    do_it = input(question + " (y/n)\n").lower()
    while not re.match("^([yjn]|yes|no)$", do_it):
        do_it = input("Please type y(es) or n(o):\n")
    if re.match("^([yj]|yes)$", do_it):
        return True
    return False


def ask_choose_from_enum(enum):
    i = 0
    entries = []
    for entry in enum:
        entries.append(entry.name)
        i += 1
        print(str(i) + "\t" + entry.name)
    entry_nr = input_require_int(input("Please select an entry:"))
    return enum[entries[entry_nr-1]]


def ask_choose_from_list_or_new(a_list):
    print("1\tNew entry")
    i = 1
    for entry in a_list:
        i += 1
        print(str(i) + "\t" + entry)
    return input_require_int(input("Please select an entry:")) - 1


def input_require_match_reqex(regex, raw_input):
    while not re.match("^[_a-zA-Z][_a-zA-Z0-9\-]*$", raw_input):
        raw_input = input("Please input a valid string as name (should match \"" + regex + "\"):\n")
    return raw_input


def input_require_int(raw_input):
    while True:
        try:
            if int(raw_input) > 0:
                return int(raw_input)
            else:
                raise ValueError
        except ValueError:
            raw_input = input("Please input a valid number\n")


class ThingArtifact(Enum):
    Attribute = 1
    Feature = 2
    Property = 3
    Action = 4
