#!/usr/bin/env python
import re


"""
This script handles the THING setup.
"""


def request_thing_name():
    """
    Asks the user for a thing name. The name has to consist of URI
    allowed characters only (http://www.ietf.org/rfc/rfc2396.txt).
    :return: uri conform string
    :rtype: basestring
    """
    raw_name = input("Please choose a name for your new thing:\n")
    while not re.match("^[a-zA-Z0-9_\-\.\!\~\*\'\(\)]*$", raw_name):
        raw_name = input("Please input a valid uri string as name:f\n")
    return raw_name


def get_thing_id(settings):
    """
    Build the thing id out of the set namespace and chosen name.
    :param settings: the settings dictionary of the thingberry
    :type settings: dict
    :return: a string containing the thing id
    :rtype: basestring
    """
    return settings["namespace"] + ":" + settings["id"]


def main():
    settings = dict()
    print("Welcome to thingberry.\nThe following steps will guide you through the setup of your new raspberry thing.")
    settings["id"] = request_thing_name()
    settings["namespace"] = "thingberry"
    print("Your things id is \"" + get_thing_id(settings) + "\".")


if __name__ == "__main__":
    main()


