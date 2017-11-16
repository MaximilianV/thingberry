import re
import json
from pathlib import Path


class Thing:
    """This class represents the thing.
    It handles settings and can start synchronization to the thing cloud.
    """
    SETTINGS_FILE = "settings.json"

    def __init__(self):
        self.settings = dict()
        self.settings["namespace"] = "thingberry"
        print("A new thing!")

    @property
    def name(self):
        return self.settings["name"]

    @name.setter
    def name(self, name):
        if not re.match("^[a-zA-Z0-9_\-\.\!\~\*\'\(\)]*$", name):
            raise ValueError
        self.settings["name"] = name

    @property
    def namespace(self):
        return self.settings["namespace"]

    def get_id(self):
        """
        Build the thing id out of the set namespace and chosen name.
        :return: a string containing the thing id
        :rtype: basestring
        """
        return self.namespace + ":" + self.name

    def write_settings(self):
        """
        Saves the settings dictionary to disk.
        """
        with open(self.SETTINGS_FILE, 'w') as fp:
            json.dump(self.settings, fp)

    def load_settings(self):
        """
        Loads settings dictionary from disk.
        """
        with open(self.SETTINGS_FILE, 'r') as fp:
            self.settings = json.load(fp)

    @staticmethod
    def do_settings_exist():
        """
        Checks whether there already is a settings file for thingberry.
        :return: whether a settings file exist
        :rtype: boolean
        """
        if Path(Thing.SETTINGS_FILE).is_file():
            return True
        return False
