#!/usr/bin/python
# -*- coding: UTF-8 -*-
from niprov.jsonfile import JsonFile


def log(new, transformation, parent, code=None, logtext=None,
        repository=JsonFile()):
    """
    Record a transformation that creates a new image.

    Args:
        new (str): Path to the newly created file.
        transformation (str): Name of the operation that has been used.
        parent (str): Path to the file that was used as the basis of the transformation

    Returns:
        dict: New provenance
    """
    provenance = {}
    provenance['parent'] = parent
    provenance['path'] = new
    provenance['transformation'] = transformation
    if code:
        provenance['code'] = code
    if logtext:
        provenance['logtext'] = logtext
    if repository.knowsByPath(parent):
        parentProvenance = repository.byPath(parent)
        provenance['acquired'] = parentProvenance['acquired']
        provenance['subject'] = parentProvenance['subject']
        provenance['protocol'] = parentProvenance['protocol']
    repository.add(provenance)
    return provenance



    
