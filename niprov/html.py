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

    def __init__(self, filesys, listener, externals):
        self.filesys = filesys
        self.listener = listener
        self.externals = externals

    def exportList(self, provenance):
        itemfmt = '<li>{0[acquired]} {0[subject]} {0[protocol]}</li>'
        with self.filesys.open('provenance.html','w') as htmlfile:
            htmlfile.write(self.header)
            htmlfile.write('<ol>')
            for provitem in provenance:
                htmlfile.write(itemfmt.format(provitem))
            htmlfile.write('</ol>')
            htmlfile.write(self.footer)
        self.externals.run(['firefox', 'provenance.html'])

