import socket, os.path


class Location(object):
    """Represents the location of a file."""

    def __init__(self, locationString):
        if ':' in locationString:
            parts = locationString.split(':')
            self.hostname = parts[0]
            path = parts[1]
        else:
            self.hostname = socket.gethostname()
            path = locationString
        self.path = os.path.abspath(path)

    def toDictionary(self):
        d = {}
        d['path'] = self.path
        d['hostname'] = self.hostname
        d['location'] = str(self)
        return d

    def toUrl(self):
        return 'file://{0}{1}'.format(self.hostname, self.path)

    def __str__(self):
        return self.toString()

    def toString(self):
        return ':'.join([self.hostname, self.path])

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return str(self) == str(other)
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)
