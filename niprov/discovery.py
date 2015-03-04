#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
from niprov.filesystem import Filesystem
from niprov.commandline import Commandline
from niprov.filefilter import FileFilter
from niprov.jsonfile import JsonFile
from niprov.files import FileFactory


def discover(root, filefilter=FileFilter(), filesys=Filesystem(), 
        listener=Commandline(), repository=JsonFile(), file=FileFactory()):
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
                img = file.locatedAt(filepath)
                if repository.knows(img):
                    listener.knownFile(img.path)
                elif repository.knowsSeries(img):
                    series = repository.getSeries(img)
                    series.addFile(img)
                    repository.update(series)
                    listener.fileFoundInSeries(img, series)
                else:
                    img.inspect()
                    repository.add(img.provenance)
                    listener.fileFound(img)
       
