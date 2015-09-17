

class Location(object):

    def __init__(self, locationString):
        self.path = locationString

    def toDictionary(self):
        d = {}
        d['path'] =self.path
        return d
