#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pkg_resources
from niprov.filesystem import Filesystem


class FileFilter(object):

    def __init__(self, filesys=Filesystem()):
        filterfile = pkg_resources.resource_filename(
            'niprov','discovery-filter.txt')
        self.filters = filesys.readlines(filterfile)

    def include(self, filepath):
        """Whether the file is to be included in discovery.

        Args:
            filepath (str): The full path of the file.

        Returns:
            bool: True if the file should be included.

        Raises:
            ValueError: If not able to read discovery-filter.txt
        """
#        if not self.filters:
#            raise ValueError('Was not able to load filter file.')
        for filt in self.filters:
            if filt in filepath:
                return True
        return False
