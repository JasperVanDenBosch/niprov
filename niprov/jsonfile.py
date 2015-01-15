from niprov.filesystem import Filesystem
from jsonserializing import JsonSerializer


class JsonFile(object):
    """Stores provenance in a local text file encoded as json.
    """

    def __init__(self, filesys=Filesystem(), json=JsonSerializer()):
        self.filesys = filesys
        self.json = json

    def add(self, record):
        """Add the provenance for one file to storage.

        Args:
            record (dict): Provenance for one image file.
        """
        current = self.all()
        current.append(record)
        jsonstr = self.json.serializeList(current)
        with open('provenance.json', 'w') as fp:
            fp.write(jsonstr)

    def all(self):
        """Retrieve all known provenance from storage.

        Return:
            list: List of provenance for known files.
        """
        try:
            jsonstr = self.filesys.read('provenance.json')
        except IOError:
            return []
        return self.json.deserializeList(jsonstr)

    def byPath(self, path):
        all = self.all()
        return [r for r in all if r['path'] == path][0]

    def bySubject(self, subject):
        all = self.all()
        return [f for f in all if f['subject']==subject]

