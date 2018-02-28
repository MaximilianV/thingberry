# thingberry
This tool provides an easy way to connect your Raspberry Pi to the Bosch IoT Things service.

## Installation
1. Clone this repository to your Raspberry Pi. Please note, that thingberry is written in Python3 and will not work with Python2.
2. The `requirements.txt` lists all prerequists needed in order to run this application.
   Execute `sudo pip install -r requirements.txt` to install all dependecies automatically.
   It is recommended to do so as root user, as the [RPi.GPIO module states](https://sourceforge.net/p/raspberry-gpio-python/wiki/install/).
3. Build your needed setup, e.g. connect a Pi-Camera, buttons, ...

## Usage
### Configuration
In the `thingconnector` folder, rename `settings_tmpl.py` to `settings.py` and fill out the requested information.
### Setup
Before the Raspberry Pi can be mirrored to the Bosch Iot Things service, an initial setup process must be completed.
Run `python setup.py` in the project folder, and you will be guided through the setup process.
If you not only want to create a configuration file, but also want to connect your Pi to the service, please choose to save the current settings, as well as sending the thing to the Bosch cloud at the end of the process.
### Run monitoring
After completing the setup, the monitoring can be started.
Execute `python run.py` as root (again, due to RPi.GPIO).
Your configuration file will be analyzed, and the observer will be started accordingly.
In addition, a WebSocket connection to the Bosch IoT Things service will be established.
If a sensor registers a new value, you should now see a log entry in your terminal, as well as a change in the Bosch Thing.
