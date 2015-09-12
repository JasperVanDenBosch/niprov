from niprov.config import Configuration


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

    def getFileFactory(self):
        import niprov.files
        return niprov.files.FileFactory()

    def getFilesystem(self):
        import niprov.filesystem
        return niprov.filesystem.Filesystem()

    def getHasher(self):
        import niprov.hashing
        return niprov.hashing.Hasher()

    def getLibraries(self):
        import niprov.libraries
        return niprov.libraries.Libraries()

    def getListener(self):
        import niprov.commandline
        return niprov.commandline.Commandline(self.config)

    def getRepository(self):
        import niprov.jsonfile
        import niprov.mongo
        if self.config.database_type == 'file':
            return niprov.jsonfile.JsonFile()
        elif self.config.database_type == 'MongoDB':
            return niprov.mongo.MongoRepository()

    def getSerializer(self):
        import niprov.jsonserializing
        return niprov.jsonserializing.JsonSerializer()



