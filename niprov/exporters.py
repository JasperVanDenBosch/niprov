#!/usr/bin/python
# -*- coding: UTF-8 -*-
from niprov.dependencies import Dependencies
from niprov.html import HtmlExporter
from niprov.stdout import StandardOutputExporter
from niprov.directexporter import DirectExporter


class ExportFactory(object):

    def __init__(self, dependencies=Dependencies()):
        self.dependencies = dependencies

    def createExporter(self, medium, form):
        """
        Return an object that can publish provenance in a specific medium.

        Args:
            medium (str): One of 'stdout' or 'html' or None.
            form (str): One of 'narrative' or None
        """
        if medium is None:
            return DirectExporter(form)
        elif medium == 'html':
            return HtmlExporter(form, dependencies=self.dependencies)
        elif medium == 'stdout':
            return StandardOutputExporter(form)
        else:
            raise ValueError('Unknown medium: '+str(medium))

