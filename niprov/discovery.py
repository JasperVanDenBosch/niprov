#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
from niprov.filesystem import Filesystem
from niprov.commandline import Commandline
from niprov.filefilter import FileFilter
from niprov.inspection import inspect


def discover(root, filefilter=FileFilter(), 
        filesys=Filesystem(), listener=Commandline()):
    dirs = filesys.walk(root)
    for (root, sdirs, files) in dirs:
        for filename in files:
            filepath = os.path.join(root, filename)
            if filefilter.include(filename):
                listener.fileFound(filename)
                inspect(filepath)
    
