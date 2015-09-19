from niprov.dependencies import Dependencies


class BaseFile(object):

    def __init__(self, location, provenance=None, dependencies=Dependencies()):
        self.dependencies = dependencies
        self.listener = dependencies.getListener()
        self.filesystem = dependencies.getFilesystem()
        self.hasher = dependencies.getHasher()
        self.serializer = dependencies.getSerializer()
        self.location = dependencies.getLocationFactory().fromString(location)
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
        Attach the current provenance to the file by saving it encoded 
        in a small textfile alongside it.

        The resulting file's name is like the file it describes,
        but with the .provenance extension.
        """
        provstr = self.serializer.serialize(self.provenance)
        self.filesystem.write(self.path+'.provenance', provstr)

    def getSeriesId(self):
        pass
