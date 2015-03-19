#!/usr/bin/python
# -*- coding: UTF-8 -*-
from niprov.filesystem import Filesystem
from niprov.commandline import Commandline
from niprov.html import HtmlExporter
from niprov.stdout import StandardOutputExporter
from niprov.directexporter import DirectExporter
from niprov.externals import Externals


class ExportFactory(object):

    def __init__(self):
        self.listener = Commandline()
        self.filesys = Filesystem()

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
            return HtmlExporter(form, self.filesys, self.listener, Externals())
        elif medium == 'stdout':
            return StandardOutputExporter(form)
        else:
            raise ValueError('Unknown medium: '+str(medium))

