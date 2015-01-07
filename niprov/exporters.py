#!/usr/bin/python
# -*- coding: UTF-8 -*-
from niprov.filesystem import Filesystem
from niprov.commandline import Commandline
from niprov.html import HtmlExporter
from niprov.externals import Externals


class ExportFactory(object):

    def __init__(self):
        self.listener = Commandline()
        self.filesys = Filesystem()

    def createExporter(self, format):
        return HtmlExporter(self.filesys, self.listener, Externals())
