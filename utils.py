import re
from enum import Enum

def ask_yes_no_question(question):
    do_it = input(question + " (y/n)\n").lower()
    while not re.match("^([yjn]|yes|no)$", do_it):
        do_it = input("Please type y(es) or n(o):\n")
    if re.match("^([yj]|yes)$", do_it):
        return True
    return False


def input_require_match_reqex(regex, raw_input):
    while not re.match(regex, raw_input):
        raw_input = input("Please input a valid string as name (should match \"" + regex + "\"):\n")
    return raw_input


class ThingArtifact(Enum):
    Attribute = 1
    Feature = 2
    Property = 3
