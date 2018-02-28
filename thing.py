import re
import json
from pathlib import Path
from thingconnector import ThingConnector, settings
from component.components import Components
from utils import ThingArtifact


class Thing:
    """This class represents the thing.
    It handles settings and can start synchronization to the thing cloud.
    """
    SETTINGS_FILE = "thing-settings.json"

    def __init__(self):
        self.settings = dict()
        self.settings["namespace"] = settings.namespace
        self.settings["features"] = {}
        self.settings["attributes"] = {}
        self.settings["actions"] = {}
        self.thingconnector = ThingConnector()
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

    @property
    def features(self):
        return self.settings["features"]

    @property
    def actions(self):
        return self.settings["actions"]

    @property
    def properties(self):
        properties = {}
        for feature in self.features:
            properties.update(self.features[feature]["properties"])
        return properties

    @property
    def attributes(self):
        return self.settings["attributes"]

    @property
    def id(self):
        """
        Build the thing id out of the set namespace and chosen name.
        :return: a string containing the thing id
        :rtype: basestring
        """
        return self.namespace + ":" + self.name

    def add_artifact(self, artifact, artifact_name, parent_artifact_name=None):
        if artifact == ThingArtifact.Feature:
            self.add_feature(artifact_name)
        if artifact == ThingArtifact.Property:
            self.add_property(parent_artifact_name, artifact_name)
        if artifact == ThingArtifact.Attribute:
            self.add_attribute(artifact_name)
        if artifact == ThingArtifact.Action:
            self.add_action(artifact_name)

    def add_feature(self, feature_name):
        self.features.update({feature_name: {'properties': {}}})

    def add_property(self, feature_name, property_name):
        self.features[feature_name]["properties"][property_name] = {"config": {}}

    def set_property_config(self, feature_name, property_name, property_config):
        self.features[feature_name]["properties"][property_name]["config"] = property_config

    def get_property_config(self, feature_name, property_name):
        return self.features[feature_name]["properties"][property_name]["config"]

    def add_action(self, action_name):
        self.actions.update({action_name: {'config': {}}})

    def set_action_config(self, action_name, action_config):
        self.actions[action_name]["config"] = action_config

    def get_action_config(self, action_name):
        return self.actions[action_name]["config"]

    def add_attribute(self, attribute_name):
        self.attributes.update({attribute_name: {}})

    def update_property(self, feature_name, property_name, value):
        if not isinstance(value, bool):
            if str(value) == str(self.get_current_property_value(feature_name, property_name)):
                return
            print("THING: Update value for \"" + feature_name + "/" + property_name + "\" to " + str(value) + ".")
            self.features[feature_name]["properties"][property_name]["value"] = str(value)
            self.thingconnector.update_property(self.id, feature_name, property_name, value)
        else:
            if value:
                current_count = int(self.features[feature_name]["properties"][property_name]["value"]) + 1
                print("THING: Update value for \"" + feature_name + "/" + property_name + "\" to " + str(current_count) + ".")
                self.features[feature_name]["properties"][property_name]["value"] = str(current_count)
                self.thingconnector.update_property(self.id, feature_name, property_name, str(current_count))

    def get_list_of_features(self):
        feature_list = []
        for feature in self.features:
            feature_list.append(feature)
        return feature_list

    def get_current_property_value(self, feature_name, property_name):
        return self.features[feature_name]["properties"][property_name]["value"]

    def get_features_without_values(self):
        features = {}
        for feature in self.features:
            features.update({feature: {"properties": {}}})
            for f_property in self.features[feature]["properties"]:
                features[feature]["properties"].update({f_property: {}})
        if self.actions:
            features.update({"actions": {"properties": {}}})
        for action in self.actions:
            features["actions"]["properties"].update({action: False})
        return features

    def get_actions(self):
        actions = dict()
        for action in self.actions:
            actions[action] = self.get_action_object(action)
        return actions

    def get_action_object(self, action_name):
        action_config = self.get_action_config(action_name)
        action_object = Components[action_config["type"]].value(thing_id=self.id)
        action_object.init_action(action_name=action_name, action_config=action_config)
        return action_object

    def get_observers(self):
        observers = dict()
        for feature in self.features:
            for f_property in self.features[feature]["properties"]:
                observers[f_property] = self.get_observer_object(feature, f_property)
        return observers

    def get_observer_object(self, feature_name, property_name):
        observer_config = self.get_property_config(feature_name, property_name)
        observer_object = Components[observer_config["type"]].value(thing_id=self.id)
        observer_object.init_observer(feature_name=feature_name, property_name=property_name, property_config=observer_config)
        return observer_object

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

    def create(self):
        print(self.thingconnector.create_thing(self))

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
