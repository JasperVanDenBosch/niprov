#!/usr/bin/python
# -*- coding: UTF-8 -*-
from niprov.filesystem import Filesystem
from niprov.commandline import Commandline
from niprov.filefilter import FileFilter
from niprov.inspection import inspect


def discover(root, filefilter=FileFilter(), 
        filesys=Filesystem(), listener=Commandline()):
    dirs = filesys.walk(root)
    for (root, sdirs, files) in dirs:
        for filepath in files:
            if filefilter.include(filepath):
                listener.fileFound(filepath)
                inspect(filepath)
    
