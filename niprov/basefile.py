from niprov.dependencies import Dependencies


class BaseFile(object):

    def __init__(self, fpath, provenance=None, dependencies=Dependencies()):
        self.path = fpath
        if provenance:
            self.provenance = provenance
            if 'path' not in provenance:
                self.provenance['path'] = self.path
        else:
            self.provenance = {'path':self.path}
        self.dependencies = dependencies
        self.listener = dependencies.getListener()
        self.filesystem = dependencies.getFilesystem()
        self.hasher = dependencies.getHasher()
        self.serializer = dependencies.getSerializer()

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
