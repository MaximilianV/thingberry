import settings
import requests
import json

BASE_URL = "https://things.apps.bosch-iot-cloud.com/api/2"
THINGS_URI = "/things/{thingId}"
FEATURES_URI = "/features/{featureName}"
PROPERTIES_URI = "/properties/{propertyName}"


class ThingConnector:

    def __init__(self):
        self.session = requests.Session()
        self.session.auth = (settings.username, settings.password)
        self.session.headers.update({'x-cr-api-token': settings.api_token,
                                     'Content-Type': 'application/json'})

    def create_thing(self, thing):
        uri = THINGS_URI.format(thingId=thing.get_id())
        data = {'thingId': thing.get_id(),
                'policyId': thing.get_id(),
                'attributes': thing.attributes,
                'features': thing.get_features_without_values()}
        return ThingConnector.get_response_message(self.put(uri, data), "thing")

    def update_property(self, thing_id, feature_name, property_name, value):
        uri = THINGS_URI.format(thingId=thing_id)\
              + FEATURES_URI.format(featureName=feature_name)\
              + PROPERTIES_URI.format(propertyName=property_name)
        data = str(value)
        return ThingConnector.get_response_message(self.put(uri, data), "thing")

    def put(self, uri, data):
        r = self.session.put(ThingConnector.build_url(uri), json=data)
        return r

    @staticmethod
    def build_url(uri):
        return BASE_URL + uri

    @staticmethod
    def get_response_message(request, artifact_name):
        if request.status_code == requests.codes.created:
            return "Successfully created the " + artifact_name
        if request.status_code == requests.codes.no_content:
            return "Updated or deleted the " + artifact_name
        return request.reason + "\n" + request.text