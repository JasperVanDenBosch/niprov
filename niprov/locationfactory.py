from niprov.dependencies import Dependencies
from niprov.location import Location


class LocationFactory(object):
    """Creates Location objects."""

    def __init__(self, dependencies=Dependencies()):
        self.dependencies = dependencies

    def fromString(self, locationString):
        return Location(locationString)

    def completeString(self, locationString):
        return str(self.fromString(locationString))
