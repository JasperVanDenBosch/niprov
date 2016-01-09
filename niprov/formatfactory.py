from niprov.dependencies import Dependencies
from niprov.formatjson import JsonFormat
from niprov.formatxml import XmlFormat
from niprov.formatnarrated import NarratedFormat
from niprov.formatsimple import SimpleFormat
from niprov.formatdict import DictFormat
from niprov.formatobject import ObjectFormat


class FormatFactory(object):

    def __init__(self, dependencies=Dependencies()):
        self.dependencies = dependencies

    def create(self, formatName):
        if formatName == 'json':
            return JsonFormat(self.dependencies)
        if formatName == 'xml':
            return XmlFormat(self.dependencies)
        if formatName == 'narrated':
            return NarratedFormat()
        if formatName == 'simple':
            return SimpleFormat()
        if formatName == 'dict':
            return DictFormat()
        if formatName == 'object':
            return ObjectFormat()
        raise ValueError('Unknown format: '+str(formatName))
