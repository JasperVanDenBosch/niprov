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

    def getExternals(self):
        import niprov.externals
        return niprov.externals.Externals()

    def getExportFactory(self):
        import niprov.exporters
        return niprov.exporters.ExportFactory(dependencies=self)

    def getFileFactory(self):
        import niprov.files
        return niprov.files.FileFactory(dependencies=self)

    def getFileFilter(self):
        import niprov.filefilter
        return niprov.filefilter.FileFilter(dependencies=self)

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

    def getLocationFactory(self):
        import niprov.locationfactory
        return niprov.locationfactory.LocationFactory(dependencies=self)

    def getNarrator(self):
        import niprov.narrator
        return niprov.narrator.Narrator()

    def getRepository(self):
        import niprov.jsonfile
        import niprov.mongo
        if self.config.database_type == 'file':
            return niprov.jsonfile.JsonFile(dependencies=self)
        elif self.config.database_type == 'MongoDB':
            return niprov.mongo.MongoRepository(dependencies=self)

    def getSerializer(self):
        import niprov.jsonserializing
        return niprov.jsonserializing.JsonSerializer()

