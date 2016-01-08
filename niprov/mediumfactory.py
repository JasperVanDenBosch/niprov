from niprov.dependencies import Dependencies
from niprov.mediumstdout import StandardOutputMedium
from niprov.mediumdirect import DirectMedium


class MediumFactory(object):

    def __init__(self, dependencies=Dependencies()):
        self.dependencies = dependencies

    def create(self, mediumName):
        if mediumName == 'stdout':
            return StandardOutputMedium()
        if mediumName == 'direct':
            return DirectMedium()
        raise ValueError('Unknown medium: '+str(mediumName))

