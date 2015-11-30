import os


class Pipeline(object):

    def __init__(self, files):
        self.files = files
        self.roots = set([f for f in files if f.parents == []])
        def locationBranchRecurse(image):
            branch = {}
            loc = image.location.toString()
            children = [f for f in files if loc in f.parents]
            for child in children:
                branch[child.location.toString()] = locationBranchRecurse(child)
            return branch
        self.locationTree = {}
        for f in self.roots:
            self.locationTree[f.location.toString()] = locationBranchRecurse(f)

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




