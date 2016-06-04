from niprov.format import Format
import io, os

_CACHE = {}

class PictureCache(Format):

    def __init__(self, dependencies):
        cachedir = os.path.expanduser('~/.niprov-snapshots')
        if not os.path.isdir(cachedir):
            os.mkdir(cachedir)

    def new(self):
        return io.BytesIO()

    def keep(self, picture, for_):
        imgId = for_.provenance['id']
        picture.seek(0)
        bytes = picture.read()
        _CACHE[imgId] = bytes

    def getBytes(self, for_):
        imgId = for_.provenance['id']
        if imgId in _CACHE:
            return _CACHE[imgId]
        return None

    def getFilepath(self, for_):
        return self.saveToDisk(for_)

    def saveToDisk(self, for_):
        imgId = for_.provenance['id']
        if not imgId in _CACHE:
            return
        fpath = os.path.expanduser('~/.niprov-snapshots/{}.png'.format(imgId))
        if not os.path.isfile(fpath):
            with open(fpath, 'w') as picfile:
                picfile.write(_CACHE[imgId])
        return fpath

    def serializeSingle(self, image):
        """Provides file path to picture of image.

        This is part of the :class:`.Format` interface. 
        """
        return self.getFilepath(for_=image)

