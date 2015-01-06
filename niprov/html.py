#!/usr/bin/python
# -*- coding: UTF-8 -*-


class HtmlExporter(object):

    def __init__(self, filesys, listener, externals):
        self.filesys = filesys
        self.listener = listener
        self.externals = externals

    def exportList(self, provenance):
        itemfmt = '<li>{0[acquired]} {0[subject]} {0[protocol]}</li>'
        with self.filesys.open('provenance.html','w') as htmlfile:
            htmlfile.write('<ol>')
            for provitem in provenance:
                htmlfile.write(itemfmt.format(provitem))
            htmlfile.write('</ol>')
        self.externals.run(['firefox', 'provenance.html'])

