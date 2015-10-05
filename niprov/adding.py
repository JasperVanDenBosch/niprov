#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os, errno
import shortuuid
from datetime import datetime
from niprov.dependencies import Dependencies


def add(filepath, transient=False, provenance=None, 
    dependencies=Dependencies()):
    """
    Simply register the file.

    Inspects the file and makes it known to the provenance data, such that 
    image files can be logged that have been created using this file. 
    Useful also for temporary files.
    
    Example:
        (provenance, status) = niprov.add('/path/to/my.nii')

    Args:
        filepath (str): Path to the newly created file.
        transient (bool, optional): Set this to True to indicate that the file 
            is only temporary and future checks should not expect it to be 
            physically present. Defaults to False, assuming that the file 
            remains.
        provenance (dict, optional): Add the key-value pairs in this dictionary 
            to the provenance record for the new file.

    Returns:
        tuple: Tuple of new provenance and status. Status is a string with one 
            of the following values:
            'new': File was not known yet and has been added.
            'series': The file was deemed part of a series and has been added.
            'failed': There was an error inspecting the file.
            'known': The file was already known to niprov, nothing happened.
            'dryrun': Function called with opts.dryrun, database not touched.
    """
    opts = dependencies.getConfiguration()
    file = dependencies.getFileFactory()
    repository = dependencies.getRepository()
    listener = dependencies.getListener()
    filesys = dependencies.getFilesystem()

    if provenance is None:
        provenance = {}
    provenance['transient'] = transient
    provenance['added'] = datetime.now()
    provenance['id'] = shortuuid.uuid()[:6]

    filepath = os.path.abspath(filepath)
    img = file.locatedAt(filepath, provenance=provenance)
    if opts.dryrun:
        status = 'dryrun'
    elif repository.knows(img):
        listener.knownFile(img.path)
        status = 'known'
    elif repository.knowsSeries(img):
        series = repository.getSeries(img)
        series.addFile(img)
        repository.update(series)
        listener.fileFoundInSeries(img, series)
        status = 'series'
    else:
        if not transient:
            if not filesys.fileExists(filepath):
                raise IOError(errno.ENOENT, 'File not found', filepath)
            try:
                img.inspect()
            except:
                listener.fileError(img.path)
                status = 'failed'
                return (img, status)
        repository.add(img)
        listener.fileFound(img)
        status = 'new'
    return (img, status)



    
