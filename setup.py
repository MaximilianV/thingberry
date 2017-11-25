#!/usr/bin/env python
import re
from thing import Thing
import utils
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
        raw_name = input("Please input a valid uri string as name:\n")
    return raw_name


def request_should_import_existing_settings():
    return utils.ask_yes_no_question("Do you want to import it?")


def request_should_save_settings():
    return utils.ask_yes_no_question("Do you want to save your current settings?")


def request_should_send_to_bosch():
    return utils.ask_yes_no_question("Should the thing be send to the Bosch cloud?")


def setup_new_thing(thing):
    print("The following steps will guide you through the setup of your new raspberry thing.")
    thing.name = request_thing_name()
    print("Your things id is \"" + thing.get_id() + "\".")


def main():
    thing = Thing()
    print("Welcome to thingberry.")
    if thing.do_settings_exist():
        print("An existing settings file was found.")
        if request_should_import_existing_settings():
            thing.load_settings()
            print("Successfully loaded settings for thing " + thing.name)
        else:
            print("Please keep in mind, that your existing settings will be overwritten.")
            setup_new_thing(thing)
    else:
        setup_new_thing(thing)

    print("You finished the setup.")

    if request_should_save_settings():
        thing.write_settings()
        print("Wrote settings to disk.")

    if request_should_send_to_bosch():
        thing.create()
        print("Sent thing to the clouds!")

    print("Bye.")


if __name__ == "__main__":
    main()


