#!/usr/bin/python
# -*- coding: UTF-8 -*-
from niprov.filesystem import Filesystem
from niprov.commandline import Commandline

def discover(root, filesys=Filesystem(), listener=Commandline()):
    dirs = filesys.walk(root)
    for (root, sdirs, files) in dirs:
        for filepath in files:
            listener.fileFound(filepath)
    
