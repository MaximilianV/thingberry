from actions.action import Action
from picamera import PiCamera
from time import sleep


class PhotoAction(Action):
    def trigger(self, delay=2, destination=None):
        print("Taking a photo in " + str(delay) + " seconds.")
        camera = PiCamera()
        sleep(delay)
        camera.capture(destination)
