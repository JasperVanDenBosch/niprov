#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
from niprov.filesystem import Filesystem


packageroot = os.path.split(os.path.split(__file__)[0])[0]
defaultfilterfile = os.path.join(packageroot,'discovery-filter.txt')

class FileFilter(object):

    def __init__(self, filesys=Filesystem()):
        try:
            self.filters = filesys.readlines(defaultfilterfile)
        except:
            self.filters = None

    def include(self, filepath):
        """Whether the file is to be included in discovery.

        Args:
            filepath (str): The full path of the file.

        Returns:
            bool: True if the file should be included.

        Raises:
            ValueError: If not able to read discovery-filter.txt
        """
        if not self.filters:
            raise ValueError('Was not able to load filter file.')
        for filt in self.filters:
            if filt in filepath:
                return True
        return False
