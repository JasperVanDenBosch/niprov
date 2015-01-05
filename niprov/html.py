#!/usr/bin/python
# -*- coding: UTF-8 -*-


class HtmlExporter(object):

    def __init__(self, filesys, log):
        self.filesys = filesys
        self.log = log

    def exportList(self, provenance):
        itemfmt = '<li>{0[acquired]} {0[subject]} {0[protocol]}</li>'
        with self.filesys.open() as htmlfile:
            for provitem in provenance:
                htmlfile.write(itemfmt.format(provitem))

