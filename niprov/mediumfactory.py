from niprov.dependencies import Dependencies
from niprov.mediumstdout import StandardOutputMedium
from niprov.mediumdirect import DirectMedium
from niprov.mediumfile import FileMedium
from niprov.mediumviewer import ViewerMedium


class MediumFactory(object):

    def __init__(self, dependencies=Dependencies()):
        self.dependencies = dependencies

    def create(self, mediumName):
        if mediumName == 'stdout':
            return StandardOutputMedium()
        if mediumName == 'direct':
            return DirectMedium()
        if mediumName == 'file':
            return FileMedium(self.dependencies)
        if mediumName == 'viewer':
            return ViewerMedium(self.dependencies)
        raise ValueError('Unknown medium: '+str(mediumName))

