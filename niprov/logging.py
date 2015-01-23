#!/usr/bin/python
# -*- coding: UTF-8 -*-
from niprov.jsonfile import JsonFile


def log(transformation, ancestor, new, code=None, logtext=None,
        repository=JsonFile()):
    """
    Record a transformation that creates a new image.

    Args:
        transformation (str): Name of the operation that has been used.
        ancestor (str): Path to the file that was used as the basis of the transformation
        new (str): Path to the newly created file.

    Returns:
        dict: New provenance
    """
    provenance = {}
    provenance['ancestor'] = ancestor
    provenance['path'] = new
    provenance['transformation'] = transformation
    if code:
        provenance['code'] = code
    if logtext:
        provenance['logtext'] = logtext
    if repository.knowsByPath(ancestor):
        ancestorProvenance = repository.byPath(ancestor)
        provenance['acquired'] = ancestorProvenance['acquired']
        provenance['subject'] = ancestorProvenance['subject']
        provenance['protocol'] = ancestorProvenance['protocol']
    repository.add(provenance)
    return provenance



    
