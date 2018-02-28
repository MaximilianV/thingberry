import re
from enum import Enum


def ask_yes_no_question(question):
    """
    Asks the user to answer the given question with yes or no.
    Yes, Y, No and N are accepted as valid responses (case insensitive).
    :param question: the question to be answered
    :type question: str
    :return: the user's answer
    :rtype: bool
    """
    do_it = input(question + " (y/n)\n").lower()
    while not re.match("^([yjn]|yes|no)$", do_it):
        do_it = input("Please type y(es) or n(o):\n")
    if re.match("^([yj]|yes)$", do_it):
        return True
    return False


def ask_choose_from_enum(enum):
    """
    Asks the user to choose an element of a given enum.
    :param enum: the enum to choose from
    :type enum: enumeration
    :return: the chosen enum element
    :rtype: enumeration member
    """
    i = 0
    entries = []
    for entry in enum:
        entries.append(entry.name)
        i += 1
        print(str(i) + "\t" + entry.name)
    entry_nr = input_require_int(input("Please select an entry:"))
    return enum[entries[entry_nr-1]]


def ask_choose_index_from_list_or_new(a_list):
    """
    Asks the user to choose an element from a given list or whether the user wants to create a new entry.
    :param a_list: the list to choose from
    :type a_list: list
    :return: the chosen index (if "new entry" is selected, return None)
    :rtype: int, None
    """
    print("1\tNew entry")
    i = 1
    for entry in a_list:
        i += 1
        print(str(i) + "\t" + entry)
    index = input_require_int(input("Please select an entry:")) - 1
    if index == 0:
        return None
    return index - 1


def input_require_match_reqex(regex, raw_input):
    """
    Utility function that requires a given input to match a given regular expression.
    In case the expression is not met, ask the user to repeat the input in a valid format.
    :param regex: the regular expression the input should be checked with
    :type regex: str
    :param raw_input: the initial input to check
    :type raw_input: str
    :return: the user input matching the given expression
    :rtype: str
    """
    while not re.match("^[_a-zA-Z][_a-zA-Z0-9\-]*$", raw_input):
        raw_input = input("Please input a valid string as name (should match \"" + regex + "\"):\n")
    return raw_input


def input_require_int(raw_input):
    """
    Utility function that requires a given input to be an integer greater zero.
    In case the given input is not an integer or zero or negative, the user is requested to provide a valid input.
    :param raw_input: the initial user input
    :type raw_input: str
    :return: a number greater zero the user inserted
    :rtype: int
    """
    while True:
        try:
            if int(raw_input) > 0:
                return int(raw_input)
            else:
                raise ValueError
        except ValueError:
            raw_input = input("Please input a valid number\n")


class ThingArtifact(Enum):
    """
    This enum defines what different kind of artifacts a Thing can have and is used during setup process to
    simplify the code.
    """
    Attribute = 1
    Feature = 2
    Property = 3
    Action = 4
