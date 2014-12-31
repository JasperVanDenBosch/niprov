#!/usr/bin/python
# -*- coding: UTF-8 -*-


class ExportFactory(object):

    def createExporter(self, format):
        raise ValueError('Not implemented: '+str(format))
