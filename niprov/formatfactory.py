from niprov.dependencies import Dependencies
from niprov.jsonserializing import JsonSerializer


class FormatFactory(object):

    def __init__(self, dependencies=Dependencies()):
        self.dependencies = dependencies

    def create(self, formatName):
        return JsonSerializer(self.dependencies)
