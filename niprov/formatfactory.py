from niprov.dependencies import Dependencies
from niprov.jsonserializing import JsonSerializer
from niprov.formatxml import XmlFormat
from niprov.formatnarrated import NarratedFormat
from niprov.formatsimple import SimpleFormat


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
        if formatName == 'simple':
            return SimpleFormat()
        raise ValueError('Unknown format: '+str(formatName))
