from niprov.dependencies import Dependencies
from niprov.location import Location


class LocationFactory(object):
    """Creates Location objects."""

    def __init__(self, dependencies=Dependencies()):
        self.dependencies = dependencies

    def fromString(self, locationString):
        """Creates a Location object.
        
        Args:
            locationString (str): String with path and optionally computer id. 
        """
        return Location(locationString)

    def completeString(self, locationString):
        """Validates a location string.
        
        If locationString only contains a filesystem path, computer info will
        be added.
        """
        return str(self.fromString(locationString))
