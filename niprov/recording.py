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
    repository.add(provenance)
    return provenance



    
