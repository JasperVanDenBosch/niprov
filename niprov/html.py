#!/usr/bin/python
# -*- coding: UTF-8 -*-
from mako.lookup import TemplateLookup
import pkg_resources as pkgr
from niprov.exporter import BaseExporter


class HtmlExporter(BaseExporter):

    def __init__(self, form, dependencies):
        super(HtmlExporter, self).__init__(form, dependencies=dependencies)
        self.filesys = dependencies.getFilesystem()
        self.listener = dependencies.getListener()
        self.externals = dependencies.getExternals()
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

    def exportSingle(self, img):
        """Publish the provenance for one image in an html file and display in Firefox.

        Args:
            provenance (dict): Provenance for one image file
        """
        template = self.templates.get_template('single.mako')
        with self.filesys.open('provenance.html','w') as htmlfile:
            htmlfile.write(template.render(provenance=img.provenance))
        self.externals.run(['firefox', 'provenance.html'])

