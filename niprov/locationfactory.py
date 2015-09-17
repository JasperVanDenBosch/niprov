from niprov.dependencies import Dependencies
from niprov.location import Location


class LocationFactory(object):

    def __init__(self, dependencies=Dependencies()):
        self.dependencies = dependencies

    def fromString(self, locationString):
        return Location(locationString)
