from niprov.filesystem import Filesystem
from jsonserializing import JsonSerializer
import os


class JsonFile(object):
    """Stores provenance in a local text file encoded as json.
    """

    def __init__(self, filesys=Filesystem(), json=JsonSerializer()):
        self.filesys = filesys
        self.json = json
        self.datafile = os.path.expanduser(os.path.join('~','provenance.json'))

    def add(self, record):
        """Add the provenance for one file to storage.

        Args:
            record (dict): Provenance for one image file.
        """
        current = self.all()
        current.append(record)
        jsonstr = self.json.serializeList(current)
        with open(self.datafile, 'w') as fp:
            fp.write(jsonstr)

    def all(self):
        """Retrieve all known provenance from storage.

        Return:
            list: List of provenance for known files.
        """
        try:
            jsonstr = self.filesys.read(self.datafile)
        except IOError:
            return []
        return self.json.deserializeList(jsonstr)

    def knowsByPath(self, path):
        """Whether the file at this path has provenance associated with it.

        Return:
            bool: True if provenance is available for that path.
        """
        try:
            self.byPath(path)
        except IndexError:
            return False
        return True

    def byPath(self, path):
        all = self.all()
        return [r for r in all if r['path'] == path][0]

    def bySubject(self, subject):
        all = self.all()
        return [f for f in all if f['subject']==subject]

