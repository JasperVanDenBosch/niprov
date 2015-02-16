#!/usr/bin/python
# -*- coding: UTF-8 -*-
from niprov.jsonfile import JsonFile


def log(new, transformation, parents, code=None, logtext=None,
        repository=JsonFile()):
    """
    Record a transformation that creates a new image.

    Args:
        new (str): Path to the newly created file.
        transformation (str): Name of the operation that has been used.
        parents (str): Paths to the files that were used as the basis of the 
            transformation. Assumes that the first file in the list is the 
            primary parent for which basic provenance is known.

    Returns:
        dict: New provenance
    """
    provenance = {}
    provenance['parents'] = parents
    provenance['path'] = new
    provenance['transformation'] = transformation
    if code:
        provenance['code'] = code
    if logtext:
        provenance['logtext'] = logtext
    if repository.knowsByPath(parents[0]):
        parentProvenance = repository.byPath(parents[0])
        provenance['acquired'] = parentProvenance['acquired']
        provenance['subject'] = parentProvenance['subject']
        provenance['protocol'] = parentProvenance['protocol']
    repository.add(provenance)
    return provenance



    
