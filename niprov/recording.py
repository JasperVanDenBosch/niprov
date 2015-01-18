#!/usr/bin/python
# -*- coding: UTF-8 -*-
from niprov.jsonfile import JsonFile


def record(ancestor, new, transformation, repository=JsonFile()):
    """
    Record an transformation that creates a new image.
    """
    provenance = {}
    provenance['ancestor'] = ancestor
    provenance['path'] = new
    provenance['transformation'] = transformation
    if repository.knowsByPath(ancestor):
        ancestorProvenance = repository.byPath(ancestor)
        provenance['acquired'] = ancestorProvenance['acquired']
        provenance['subject'] = ancestorProvenance['subject']
        provenance['protocol'] = ancestorProvenance['protocol']
    repository.add(provenance)
    return provenance



    
