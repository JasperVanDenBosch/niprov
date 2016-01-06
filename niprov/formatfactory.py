from niprov.dependencies import Dependencies
from niprov.jsonserializing import JsonSerializer
from niprov.formatxml import XmlFormat


class FormatFactory(object):

    def __init__(self, dependencies=Dependencies()):
        self.dependencies = dependencies

    def create(self, formatName):
        if formatName == 'json':
            return JsonSerializer(self.dependencies)
        elif formatName == 'xml':
            return XmlFormat(self.dependencies)
