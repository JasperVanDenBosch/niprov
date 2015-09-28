#!/usr/bin/python
# -*- coding: UTF-8 -*-
from niprov.dependencies import Dependencies


class FileFilter(object):

    def __init__(self, dependencies=Dependencies()):
        config = dependencies.getConfiguration()
        self.filters = config.discover_file_extensions

    def include(self, filepath):
        """Whether the file is to be included in discovery.

        Args:
            filepath (str): The full path of the file.

        Returns:
            bool: True if the file should be included.
        """
        for filt in self.filters:
            if filt in filepath:
                return True
        return False
