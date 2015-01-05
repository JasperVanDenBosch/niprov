import os


class Filesystem():

    def __init__(self):
        self.open = open

    def walk(self, path):
        return os.walk(path)

    def readlines(self, path):
        with open(path) as fhandle:
            lines = fhandle.read().splitlines()
        return lines

