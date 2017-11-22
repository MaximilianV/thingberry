import settings
import requests

BASE_URL = "https://things.apps.bosch-iot-cloud.com/api/2/"
THINGS_URI = "things/{thingId}"


class ThingConnector:

    def create_thing(self, thing_id):
        uri = THINGS_URI.format(thingId=thing_id)
        self.put(uri)

    def put(self, uri):
        headers = {'x-cr-api-token': settings.api_token}
        r = requests.get(ThingConnector.build_url(uri), headers, auth=(settings.username, settings.password))
        print(r.json())

    @staticmethod
    def get_header():
        return

    @staticmethod
    def build_url(uri):
        return BASE_URL + uri
