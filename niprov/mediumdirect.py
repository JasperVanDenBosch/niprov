#!/usr/bin/python
# -*- coding: UTF-8 -*-


class DirectMedium(object):
    """Dummy  Medium class which simply returns the serialized provenance 
    passed.
    """

    def export(self, formattedProvenance, form):
        return formattedProvenance

