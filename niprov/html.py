#!/usr/bin/python
# -*- coding: UTF-8 -*-


class HtmlExporter(object):

    header = """
<html>
<head>
<style>
html {font-family:arial;}
li{ margin: 10px;}
li:hover{color:blue;}
</style>
<title>Provenance</title>
</head>
<h1>Provenance</h1>
"""
    footer = '</html>'
    expectedFields = ['acquired','subject','protocol']

    def __init__(self, filesys, listener, externals):
        self.filesys = filesys
        self.listener = listener
        self.externals = externals

    def exportList(self, provenance):
        itemfmt = '<li>{0[acquired]} {0[subject]} {0[protocol]} {1}</li>'
        with self.filesys.open('provenance.html','w') as htmlfile:
            htmlfile.write(self.header)
            htmlfile.write('<ol>')
            for provitem in provenance:
                for field in self.expectedFields:
                    if not (field in provitem):
                        provitem[field] = '?'
                path = provitem['path']
                if len(path) > 42:
                    path = '..'+path[-40:]
                htmlfile.write(itemfmt.format(provitem, path))
            htmlfile.write('</ol>')
            htmlfile.write(self.footer)
        self.externals.run(['firefox', 'provenance.html'])

