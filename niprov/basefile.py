from niprov.dependencies import Dependencies


class BaseFile(object):

    def __init__(self, location, provenance=None, dependencies=Dependencies()):
        self.dependencies = dependencies
        self.listener = dependencies.getListener()
        self.filesystem = dependencies.getFilesystem()
        self.hasher = dependencies.getHasher()
        self.serializer = dependencies.getSerializer()
        self.location = dependencies.getLocationFactory().fromString(location)
        self.formats = dependencies.getFormatFactory()
        if provenance:
            self.provenance = provenance
        else:
            self.provenance = {}
        self.provenance.update(self.location.toDictionary())
        self.path = self.provenance['path']

    def inspect(self):
        self.provenance['size'] = self.filesystem.getsize(self.path)
        self.provenance['created'] = self.filesystem.getctime(self.path)
        self.provenance['hash'] = self.hasher.digest(self.path)
        return self.provenance

    def attach(self):
        """
        Not implemented for BaseFile parent class.
        """
        pass

    def getProvenance(self, form):
        return self.formats.create(form).serialize(self)

    def getSeriesId(self):
        pass

    @property
    def parents(self):
        return self.provenance.get('parents', [])
