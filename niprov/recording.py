#!/usr/bin/python
# -*- coding: UTF-8 -*-

def record(ancestor, new, transformation):
    """
    Record an transformation that creates a new image.
    """
    provenance = {}
    provenance['ancestor'] = ancestor
    provenance['path'] = new
    provenance['transformation'] = transformation
    return provenance



    
