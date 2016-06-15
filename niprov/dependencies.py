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

    def getCamera(self):
        import niprov.camera
        return niprov.camera.Camera(dependencies=self)

    def getClock(self):
        import niprov.clock
        return niprov.clock.Clock()

    def getConfiguration(self):
        return self.config

    def getExternals(self):
        import niprov.externals
        return niprov.externals.Externals()

    def getFileFactory(self):
        import niprov.files
        return niprov.files.FileFactory(dependencies=self)

    def getFileFilter(self):
        import niprov.filefilter
        return niprov.filefilter.FileFilter(dependencies=self)

    def getFilesystem(self):
        import niprov.filesystem
        return niprov.filesystem.Filesystem()

    def getFormatFactory(self):
        import niprov.formatfactory
        return niprov.formatfactory.FormatFactory(dependencies=self)

    def getHasher(self):
        import niprov.hashing
        return niprov.hashing.Hasher()

    def getLibraries(self):
        import niprov.libraries
        return niprov.libraries.Libraries()

    def getListener(self):
        import niprov.commandline
        return niprov.commandline.Commandline(dependencies=self)

    def getLocationFactory(self):
        import niprov.locationfactory
        return niprov.locationfactory.LocationFactory(dependencies=self)

    def getMediumFactory(self):
        import niprov.mediumfactory
        return niprov.mediumfactory.MediumFactory(dependencies=self)

    def getRepository(self):
        import niprov.jsonfile
        import niprov.mongo
        if self.config.database_type == 'file':
            return niprov.jsonfile.JsonFile(dependencies=self)
        elif self.config.database_type == 'MongoDB':
            return niprov.mongo.MongoRepository(dependencies=self)

    def getSerializer(self):
        import niprov.formatjson
        return niprov.formatjson.JsonFormat(self)

    def getPictureCache(self):
        import niprov.pictures
        return niprov.pictures.PictureCache(dependencies=self)

    def getPipelineFactory(self):
        import niprov.pipelinefactory
        return niprov.pipelinefactory.PipelineFactory(dependencies=self)

    def getQuery(self):
        import niprov.querying
        return niprov.querying.Query(dependencies=self)

    def getUsers(self):
        import niprov.users
        return niprov.users.Users(dependencies=self)

