import socket


class Location(object):

    def __init__(self, locationString):
        if ':' in locationString:
            parts = locationString.split(':')
            self.hostname = parts[0]
            self.path = parts[1]
        else:
            self.hostname = socket.gethostname()
            self.path = locationString

    def toDictionary(self):
        d = {}
        d['path'] = self.path
        d['hostname'] = self.hostname
        return d

    def __str__(self):
        return ':'.join([self.hostname, self.path])
