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
        if hasattr(picture, 'read'):
            picture.seek(0)
            bytes = picture.read()
        else:
            bytes = str(picture)
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
        fpath = os.path.expanduser('~/.niprov-snapshots/{}.png'.format(imgId))
        if os.path.isfile(fpath):
            return fpath
        elif imgId in _CACHE:
            with open(fpath, 'w') as picfile:
                picfile.write(_CACHE[imgId])
            return fpath
        else:
            return None

    def serializeSingle(self, image):
        """Provides file path to picture of image.

        This is part of the :class:`.Format` interface. 
        """
        return self.getFilepath(for_=image)

