#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
from niprov.filesystem import Filesystem
from niprov.commandline import Commandline
from niprov.filefilter import FileFilter
from niprov.inspection import inspect
from niprov.jsonfile import JsonFile


def discover(root, filefilter=FileFilter(), filesys=Filesystem(), 
        listener=Commandline(), repository=JsonFile()):
    discovered = []
    dirs = filesys.walk(root)
    for (root, sdirs, files) in dirs:
        for filename in files:
            filepath = os.path.join(root, filename)
            if filefilter.include(filename):
                provenance = inspect(filepath)
                if provenance is not None:
                    discovered.append(provenance)
                    listener.fileFound(filename, provenance) 
    repository.store(discovered)   
