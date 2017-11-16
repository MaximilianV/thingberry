import re


def ask_yes_no_question(question):
    do_it = input(question + " (y/n)\n").lower()
    while not re.match("^([yjn]|yes|no)$", do_it):
        do_it = input("Please type y(es) or n(o):\n")
    if re.match("^([yj]|yes)$", do_it):
        return True
    return False
