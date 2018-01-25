from actions.action import Action
from picamera import PiCamera
from time import sleep
import random
import string


class PhotoAction(Action):
    def trigger(self, delay=2, destination=None, **kwargs):
        print("Taking a photo in " + str(delay) + " seconds.")
        filename = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
        filename += '.jpg'
        camera = PiCamera()
        sleep(delay)
        camera.capture(destination + filename)

    @staticmethod
    def config():
        print("Configuring Photo Action:")
        delay = int(input("Delay until photo is taken (def. 2): "))
        destination = input("\nDestination to save image: ")
        return {
            "delay": delay,
            "destination": destination
        }
