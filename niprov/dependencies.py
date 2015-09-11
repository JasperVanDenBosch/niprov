from niprov.config import Configuration
from niprov.commandline import Commandline
from niprov.jsonfile import JsonFile
from niprov.mongo import MongoRepository
from niprov.files import FileFactory


class Dependencies(object):

    def __init__(self, config=None):
        if config is None:
            config = Configuration()
        self.config = config

    def reconfigureOrGetConfiguration(self, newConfiguration):
        if newConfiguration is not None:
            self.config = newConfiguration
        return self.config

    def getConfiguration(self):
        return self.config

    def getListener(self):
        return Commandline(self.config)

    def getRepository(self):
        if self.config.database_type == 'file':
            return JsonFile()
        elif self.config.database_type == 'MongoDB':
            return MongoRepository()

    def getFileFactory(self):
        return FileFactory()
