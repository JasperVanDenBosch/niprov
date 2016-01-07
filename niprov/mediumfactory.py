from niprov.dependencies import Dependencies
from niprov.stdout import StandardOutputExporter


class MediumFactory(object):

    def __init__(self, dependencies=Dependencies()):
        self.dependencies = dependencies

    def create(self, mediumName):
        if mediumName == 'stdout':
            return StandardOutputExporter(self.dependencies)

