#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os, errno
import shortuuid
from datetime import datetime
from niprov.dependencies import Dependencies
from niprov.inheriting import inheritFrom


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
            'dryrun': Function called with config.dryrun, database not touched.
    """
    config = dependencies.getConfiguration()
    file = dependencies.getFileFactory()
    repository = dependencies.getRepository()
    listener = dependencies.getListener()
    filesys = dependencies.getFilesystem()
    query = dependencies.getQuery()

    if provenance is None:
        provenance = {}
    provenance['transient'] = transient
    provenance['added'] = datetime.now()
    provenance['id'] = shortuuid.uuid()[:6]

    img = file.locatedAt(filepath, provenance=provenance)
    if config.dryrun:
        return img

    if not transient:
        if not filesys.fileExists(img.location.path):
            raise IOError(errno.ENOENT, 'File not found', img.location.path)
        try:
            img.inspect()
        except:
            img.status = 'failed'
            listener.fileError(img.path)
            return img
        if config.attach:
            img.attach(config.attach_format)

    if not provenance.get('parents', []):
        for copy in query.copiesOf(img):
            if not copy.location == img.location:
                inheritFrom(img.provenance, copy.provenance)
                img.provenance['parents'] = [copy.location.toString()]
                img.provenance['copy-as-parent'] = True
                listener.usingCopyAsParent(copy)
                break

    previousVersion = repository.byLocation(img.location.toString())
    series = repository.getSeries(img)
    if previousVersion:
        img.keepVersionsFromPrevious(previousVersion)
    elif series:
        if series.hasFile(img):
            img.keepVersionsFromPrevious(series)
        else:
            img = series.mergeWith(img)

    if not previousVersion and not series:
        repository.add(img)
    else:
        repository.update(img)

    listener.fileAdded(img)
    return img



    
