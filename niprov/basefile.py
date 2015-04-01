from niprov.commandline import Commandline
from niprov.dependencies import Dependencies
from niprov.filesystem import Filesystem
from niprov.hashing import Hasher
from niprov.jsonserializing import JsonSerializer


class BaseFile(object):

    def __init__(self, fpath, provenance=None, listener=Commandline(), 
            filesystem=Filesystem(), hasher=Hasher(), 
            serializer=JsonSerializer()):
        self.path = fpath
        if provenance:
            self.provenance = provenance
        else:
            self.provenance = {'path':self.path}
        self.listener = listener
        self.filesystem = filesystem
        self.hasher = hasher
        self.serializer = serializer

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
