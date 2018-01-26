from thing import Thing
from thingconnector.thingwatcher import ThingWatcher

thing = Thing()
thing.load_settings()
thingwatcher = ThingWatcher(thing)
thingwatcher.start_watching()
