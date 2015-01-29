from niprov.commandline import Commandline
from niprov.dependencies import Dependencies
from niprov.filesystem import Filesystem
from niprov.hashing import Hasher


class BaseFile(object):

    def __init__(self, fpath, listener=Commandline(), 
            filesystem=Filesystem(), hasher=Hasher()):
        self.path = fpath
        self.listener = listener
        self.filesystem = filesystem
        self.hasher = hasher

    def inspect(self):
        provenance = {}
        provenance['path'] = self.path
        provenance['size'] = self.filesystem.getsize(self.path)
        provenance['created'] = self.filesystem.getctime(self.path)
        provenance['hash'] = self.hasher.digest(self.path)
        return provenance
