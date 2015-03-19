#!/usr/bin/python
# -*- coding: UTF-8 -*-


class DirectExporter(object):
    """Dummy  Exporter class which simply returns the provenance passed.
    """

    def __init__(self, **kwargs):
        pass

    def exportList(self, provenance):
        return provenance

    def export(self, provenance):
        return provenance
