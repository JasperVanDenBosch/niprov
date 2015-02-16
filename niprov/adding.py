#!/usr/bin/python
# -*- coding: UTF-8 -*-
from niprov.jsonfile import JsonFile


def add(new, transient=False, repository=JsonFile()):
    """
    Simply register the file.

    This does not add any significant provenance for this file, but makes it 
    known to the provenance data, such that image files can be logged that have 
    been created using this file. Useful i.e. for temporary files.

    Args:
        new (str): Path to the newly created file.
        transient (bool, optional): Set this to True to indicate that the file 
            is only temporary and future checks should not expect it to be 
            physically present. Defaults to False, assuming that the file 
            remains.

    Returns:
        dict: New provenance
    """
    provenance = {}
    provenance['path'] = new
    provenance['transient'] = transient
    repository.add(provenance)
    return provenance



    
