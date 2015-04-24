#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
from niprov.filesystem import Filesystem
from niprov.commandline import Commandline
from niprov.filefilter import FileFilter
from niprov.adding import add


def discover(root, filefilter=FileFilter(), filesys=Filesystem(), 
        listener=Commandline()):
    """
    Search a directory for image files, and add them to your provenance collection.

    Files are only included if they match the filters in the 
    'discovery-filter.txt' file.
    Refer to niprov.add for details on what happens to individual files.

    Args:
        root (str): The top directory in which to look for new files.
    """
    dirs = filesys.walk(root)
    stats = {'total':0, 'new':0, 'series':0, 'failed':0, 'known':0}
    for (root, sdirs, files) in dirs:
        for filename in files:
            filepath = os.path.join(root, filename)
            if filefilter.include(filename):
                stats['total'] = stats['total'] + 1
                (p, status) = add(filepath, transient=False)
                stats[status] = stats[status] + 1
    listener.discoveryFinished(nnew=stats['new'], nadded=stats['series'], 
        nfailed=stats['failed'], ntotal=stats['total'])

