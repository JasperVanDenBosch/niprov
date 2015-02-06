#!/usr/bin/python
# -*- coding: UTF-8 -*-
from mako.lookup import TemplateLookup
import pkg_resources as pkgr


class HtmlExporter(object):

    _expectedFields = ['acquired','subject','protocol']
    _allfields = ['path','parent','acquired','created','subject','project','protocol',
        'transformation','code','logtext','size','hash']

    def __init__(self, filesys, listener, externals):
        self.filesys = filesys
        self.listener = listener
        self.externals = externals
        templateDir = pkgr.resource_filename('niprov', 'templates')
        self.templates = TemplateLookup([templateDir])

    def exportList(self, provenance):
        """Publish the provenance for several images in an html file and display in Firefox.

        Args:
            provenance (list): List of provenance dictionaries.
        """
        template = self.templates.get_template('list.mako')
        with self.filesys.open('provenance.html','w') as htmlfile:
            htmlfile.write(template.render(provenance=provenance))
        self.externals.run(['firefox', 'provenance.html'])

    def export(self, provenance):
        """Publish the provenance for one image in an html file and display in Firefox.

        Args:
            provenance (dict): Provenance for one image file
        """
        template = self.templates.get_template('single.mako')
        with self.filesys.open('provenance.html','w') as htmlfile:
            htmlfile.write(template.render(provenance=provenance))
        self.externals.run(['firefox', 'provenance.html'])

