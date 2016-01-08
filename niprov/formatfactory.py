from niprov.dependencies import Dependencies
from niprov.jsonserializing import JsonSerializer
from niprov.formatxml import XmlFormat
from niprov.formatnarrated import NarratedFormat


class FormatFactory(object):

    def __init__(self, dependencies=Dependencies()):
        self.dependencies = dependencies

    def create(self, formatName):
        if formatName == 'json':
            return JsonSerializer(self.dependencies)
        if formatName == 'xml':
            return XmlFormat(self.dependencies)
        if formatName == 'narrated':
            return NarratedFormat()
        raise ValueError('Unknown format: '+str(formatName))
