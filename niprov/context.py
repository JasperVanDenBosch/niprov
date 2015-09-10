from niprov.config import Configuration
from niprov.commandline import Commandline

class Context(object):

    def __init__(self):
        self.settings = Configuration()

    def getListener(self):
        return Commandline(self.settings)

    def reconfigure(self, newConfiguration):
        if newConfiguration is not None:
            self.settings = newConfiguration
