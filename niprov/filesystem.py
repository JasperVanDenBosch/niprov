import os


class Filesystem():

    def walk(self, path):
        return os.walk(path)
