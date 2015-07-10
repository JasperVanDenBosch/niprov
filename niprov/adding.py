#!/usr/bin/python
# -*- coding: UTF-8 -*-
from niprov.commandline import Commandline
from niprov.jsonfile import JsonFile
from niprov.files import FileFactory
from niprov.options import NiprovOptions


def add(filepath, transient=False, opts=NiprovOptions(), listener=Commandline(),
        repository=JsonFile(), file=FileFactory()):
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
        opts (NiprovOptions): General settings for niprov. 
            See :py:mod:`niprov.options`

    Returns:
        tuple: Tuple of new provenance and status. Status is a string with one 
            of the following values:
            'new': File was not known yet and has been added.
            'series': The file was deemed part of a series and has been added.
            'failed': There was an error inspecting the file.
            'known': The file was already known to niprov, nothing happened.
            'dryrun': Function called with opts.dryrun, database not touched.
    """
    img = file.locatedAt(filepath, provenance={'transient':transient})
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
        try:
            img.inspect()
        except:
            listener.fileError(img.path)
            status = 'failed'
        else:
            repository.add(img.provenance)
            listener.fileFound(img)
            status = 'new'
    return (img.provenance, status)



    
