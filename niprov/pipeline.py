import os


class Pipeline(object):

    def __init__(self, filesByLocation):
        self.locationTree = None

    def asFilenameTree(self):
        def toFilenameTree(d):
            new = {}
            for k, v in d.iteritems():
                if isinstance(v, dict):
                    v = toFilenameTree(v)
                newkey = os.path.basename(k.split(':')[1])
                new[newkey] = v
            return new
        return toFilenameTree(self.locationTree)




