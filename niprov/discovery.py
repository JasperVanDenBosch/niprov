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
    """
    Search a directory for image files, inspect them and store provenance.

    Files are only included if they match the filters in the 
    'discovery-filter.txt' file.
    If a file is already known, it will be ignored and the listener informed.

    Args:
        root (str): The top directory in which to look for new files.
    """
    dirs = filesys.walk(root)
    for (root, sdirs, files) in dirs:
        for filename in files:
            filepath = os.path.join(root, filename)
            if filefilter.include(filename):
                if repository.knowsByPath(filepath):
                    listener.knownFile(filepath)
                else:
                    provenance = inspect(filepath)
                    if provenance is not None:
                        repository.add(provenance)
                        listener.fileFound(filename, provenance) 
       
