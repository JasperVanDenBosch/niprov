import os


class Filesystem(object):
    """Wrapper of filesystem access functionality such as that implemented by 
    the os package in the standard library.
    """

    def __init__(self):
        self.open = open

    def walk(self, path):
        return os.walk(path)

    def readlines(self, path):
        with open(path) as fhandle:
            lines = fhandle.read().splitlines()
        return lines

    def read(self, path):
        """Read the contents of a textfile.

        Args:
            path: Path to the file to read.

        Returns:
            str: Contents of the file

        Raises:
            IOError: [Errno 2] No such file or directory: 'xyz'
        """
        with open(path) as fhandle:
            contents = fhandle.read()
        return contents

    def getsize(self, path):
        return os.path.getsize(path)

