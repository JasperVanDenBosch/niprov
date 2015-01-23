#!/usr/bin/python
# -*- coding: UTF-8 -*-
import hashlib


class Hasher(object):

    blocksize = 512*8*128

    def digest(self, filename):
        """Determine the unique hash digest for a file.

        Note: takes 26s for a 14GB file.

        Args:
            filename (str): Path to the file for which a hash digest should be made.
        """
        hash = hashlib.md5()
        with open(filename, "r+b") as f:
            for block in iter(lambda: f.read(self.blocksize), ""):
                hash.update(block)
        return hash.hexdigest()





