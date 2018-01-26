#!/usr/bin/env python
from thing import Thing
import utils
from utils import ThingArtifact
from propertyobserver.propertyobserverfactory import ObserverStyle
from propertyobserver.propertyobserver import Observer
from actions.actions import Action

"""
This script handles the THING setup.
"""

THING_NAME_REGEX = "^[a-zA-Z0-9_\-\.\!\~\*\'\(\)]*$"
FEATURE_PROPERTY_REGEX = "^[_a-zA-Z][_a-zA-Z0-9\-]*$"


def request_thing_name():
    """
    Asks the user for a thing name. The name has to consist of URI
    allowed characters only (http://www.ietf.org/rfc/rfc2396.txt).
    :return: uri conform string
    :rtype: basestring
    """
    raw_name = input("Please choose a name for your new thing:\n")
    return utils.input_require_match_reqex(THING_NAME_REGEX, raw_name)


def setup_artifacts(thing, artifact, parent_artifact=None):
    """
    This method allows to setup attributes, features and properties, depending on the provided artifact type.
    For the feature artifact, sub-properties can be created too.
    :param thing: the affected thing
    :type thing: Thing
    :param artifact: the artifact type that should be added
    :type artifact: ThingArtifact
    :param parent_artifact: default "none", name of parent feature if properties are created
    :type parent_artifact: basestring
    :return: None
    :rtype: None
    """
    print("In the following, you can configure the " + artifact.name + " of your thing.\n")
    if artifact == ThingArtifact.Feature:
        print("\"A Feature is used to manage all data and functionality of a Thing" +
              " that can be clustered in an outlined technical context.\"\n")
    if artifact == ThingArtifact.Action:
        print("\"An Action is used to control any actuator or start a script based on your thing." +
              " For example a photo can be taken each time the things camera action is updated.\"\n")
    add_artifact = True
    while add_artifact:
        setup_artifact(thing, artifact, parent_artifact)
        add_artifact = utils.ask_yes_no_question("Add another " + artifact.name + "?")


def setup_artifact(thing, artifact, parent_artifact=None):
    """
    Requests a name for the new artifact to be created and in case it is a new feature, sub-properties will be
    configurable too.
    :param thing: the affected thing
    :type thing: Thing
    :param artifact: the artifact type that should be added
    :type artifact: ThingArtifact
    :param parent_artifact: default "none", name of parent feature if properties are created
    :type parent_artifact: basestring
    :return: None
    :rtype: None
    """
    name = input("Please name the new " + artifact.name + ":\n")
    name = utils.input_require_match_reqex(FEATURE_PROPERTY_REGEX, name)
    thing.add_artifact(artifact, name, parent_artifact)
    if artifact == ThingArtifact.Feature:
        setup_artifacts(thing, ThingArtifact.Property, name)
    if artifact == ThingArtifact.Property:
        setup_property_observer(thing, name, parent_artifact)
    if artifact == ThingArtifact.Action:
        setup_action(thing, name)


def setup_property_observer(thing, property_name, feature_name):
    """
    Setup and configure a property observer (how a single property should be retrieved from the pi).
    Afterwards, this configuration is added to the thing object.
    :param thing: the affected thing
    :type thing: Thing
    :param property_name: the name for the new property
    :type property_name: basestring
    :param feature_name: the name of the feature this property belongs to
    :type feature_name: basestring
    :return: None
    :rtype: None
    """
    print("Please define how values for " + property_name + " should be obtained.")
    observer = utils.ask_choose_from_enum(Observer)
    print("Please select when values should be updated.")
    observer_style = utils.ask_choose_from_enum(ObserverStyle)
    observer_config = {}
    observer_input_config = input("Please provide the configuration for the " + observer.value.CONFIG_SPEAKING_NAME + " observer:\n")
    observer_config[observer.value.CONFIG_NAME] = observer_input_config
    thing.set_property_observer(observer_style, observer, observer_config, property_name, feature_name)


def setup_action(thing, action_name):
    """
    Let the user choose an action type and start the corresponding setup for this action.
    Afterwards, this action is added to the current thing together with its configuration.
    :param thing: the affected thing
    :type thing: Thing
    :param action_name: the name of the new action
    :type action_name: basestring
    :return: None
    :rtype: None
    """
    print("Please choose an action to be triggered:")
    action = utils.ask_choose_from_enum(Action)
    action_config = action.value.config()
    action_config["type"] = action.name
    thing.set_action(action_name, action_config)


def setup_new_thing(thing):
    """
    Starts the setup procedure for a new thing.
    :param thing: the thing object to be setup
    :type thing: Thing
    :return: None
    :rtype: None
    """
    print("The following steps will guide you through the setup of your new raspberry thing.")
    thing.name = request_thing_name()
    print("Your things id is \"" + thing.get_id() + "\".")
    setup_artifacts(thing, ThingArtifact.Feature)
    if utils.ask_yes_no_question("Does your thing has any actions (actuators)?"):
        setup_artifacts(thing, ThingArtifact.Action)


def main():
    """
    This methods leads through the whole setup process for a thing.
    :return: None
    :rtype: None
    """
    thing = Thing()
    print("Welcome to thingberry.")
    if thing.do_settings_exist():
        print("An existing settings file was found.")
        if utils.ask_yes_no_question("Do you want to import it?"):
            thing.load_settings()
            print("Successfully loaded settings for thing " + thing.name)
        else:
            print("Please keep in mind, that your existing settings will be overwritten.")
            setup_new_thing(thing)
    else:
        setup_new_thing(thing)

    print(thing.features)
    print("You finished the setup.")

    if utils.ask_yes_no_question("Do you want to save your current settings?"):
        thing.write_settings()
        print("Wrote settings to disk.")

    if utils.ask_yes_no_question("Should the thing be send to the Bosch cloud?"):
        thing.create()
        print("Sent thing to the clouds!")

    print("Bye.")


if __name__ == "__main__":
    main()


