#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
from niprov.filesystem import Filesystem


packageroot = os.path.split(os.path.split(__file__)[0])[0]
defaultfilterfile = os.path.join(packageroot,'discovery-filter.txt')

class FileFilter(object):

    def __init__(self, filesys=Filesystem()):
        self.filters = filesys.readlines(defaultfilterfile)

    def include(self, filepath):
        for filt in self.filters:
            if filt in filepath:
                return True
        return False
