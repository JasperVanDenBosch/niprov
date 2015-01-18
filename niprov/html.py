#!/usr/bin/python
# -*- coding: UTF-8 -*-


class HtmlExporter(object):

    header = """
<html>
<head>
<style>
html {font-family:arial;}
td {padding: 10px;}
tr:hover {background-color:lavender;}
</style>
<title>Provenance</title>
</head>
<h1>Provenance</h1>
<table>
<thead>
<tr>
<th>Acquired</th>
<th>Subject</th>
<th>Protocol</th>
<th>Path</th>
</tr>
</thead>
<tbody>
"""
    footer = '</html>'
    expectedFields = ['acquired','subject','protocol']

    def __init__(self, filesys, listener, externals):
        self.filesys = filesys
        self.listener = listener
        self.externals = externals

    def exportList(self, provenance):
        itemfmt = '<tr><td>{0[acquired]}</td><td>{0[subject]}</td><td>{0[protocol]}</td><td>{1}</td></tr>\n'
        with self.filesys.open('provenance.html','w') as htmlfile:
            htmlfile.write(self.header)
            #htmlfile.write('<table>')
            for provitem in provenance:
                for field in self.expectedFields:
                    if not (field in provitem):
                        provitem[field] = '?'
                path = provitem['path']
                if len(path) > 42:
                    path = '..'+path[-40:]
                htmlfile.write(itemfmt.format(provitem, path))
            htmlfile.write('</tbody></table>\n')
            htmlfile.write(self.footer)
        self.externals.run(['firefox', 'provenance.html'])

