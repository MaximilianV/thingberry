#!/usr/bin/env python
import re
import json
from pathlib import Path


"""
This script handles the THING setup.
"""

SETTINGS_FILE = "settings.json"


def request_thing_name():
    """
    Asks the user for a thing name. The name has to consist of URI
    allowed characters only (http://www.ietf.org/rfc/rfc2396.txt).
    :return: uri conform string
    :rtype: basestring
    """
    raw_name = input("Please choose a name for your new thing:\n")
    while not re.match("^[a-zA-Z0-9_\-\.\!\~\*\'\(\)]*$", raw_name):
        raw_name = input("Please input a valid uri string as name:\n")
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


def write_settings(settings):
    """
    Saves the settings dictionary to disk.
    :param settings: the settings dictionary
    :type settings: dict
    """
    with open(SETTINGS_FILE, 'w') as fp:
        json.dump(settings, fp)


def load_settings():
    """
    Loads settings dictionary from disk.
    :return: the loaded settings dictionary
    :rtype: dict
    """
    with open(SETTINGS_FILE, 'o') as fp:
        return json.load(fp)


def do_settings_exist():
    """
    Checks whether there already is a settings file for thingberry.
    :return: whether a settings file exist
    :rtype: boolean
    """
    if Path(SETTINGS_FILE).is_file():
        return True
    else:
        return False


def main():
    settings = dict()
    print("Welcome to thingberry.")
    print("The following steps will guide you through the setup of your new raspberry thing.")
    settings["id"] = request_thing_name()
    settings["namespace"] = "thingberry"
    print("Your things id is \"" + get_thing_id(settings) + "\".")


if __name__ == "__main__":
    main()


