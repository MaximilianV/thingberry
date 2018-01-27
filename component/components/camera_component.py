from component import ActionComponent
import logging
from picamera import PiCamera
from time import sleep
import random
import string


class CameraComponent(ActionComponent):
    def trigger_action(self, **kwargs):
        delay = int(self.action_config["delay"])
        if delay == 0:
            delay = 1
        destination = self.action_config["destination"]
        logging.debug("Taking a photo in " + str(delay) + " seconds.")
        filename = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
        filename += '.jpg'
        camera = PiCamera()
        sleep(delay)
        camera.capture(destination + filename)
        logging.debug("Photo taken and stored in " + str(destination) + ".")

    @staticmethod
    def configure_action():
        print("Configuring Camera Action:")
        delay = int(input("Delay until photo is taken (def. 2): "))
        destination = input("Destination to save image: ")
        return {
            "delay": delay,
            "destination": destination
        }
