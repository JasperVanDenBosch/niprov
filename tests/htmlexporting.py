import unittest
from mock import Mock
from datetime import datetime
import os
import pkg_resources as pkgr

class HtmlTests(unittest.TestCase):

    def setUp(self):
        import niprov.html
        self.log = Mock()
        self.externals = Mock()
        self.template = Mock()
        self.templateLookup = Mock()
        self.templateLookup.get_template.return_value = self.template
        self.templateLookupConstructor = Mock()
        self.img = Mock()
        self.img.provenance = {}
        niprov.html.TemplateLookup = self.templateLookupConstructor
        niprov.html.TemplateLookup.return_value = self.templateLookup
        (self.filesys, self.filehandle) = self.setupFilesys()
        self.exporter = niprov.html.HtmlExporter(None, self.filesys, self.log, 
            self.externals)

    def test_Looks_for_templates_in_right_place(self):
        self.templateLookupConstructor.assert_called_with(
            [pkgr.resource_filename('niprov', 'templates')])

    def test_ExportList_writes_output_of_renderer_to_file(self):
        self.exporter.exportList([])
        self.filesys.open.assert_called_with('provenance.html','w')
        self.filehandle.write.assert_called_with(self.template.render())

    def test_Export_writes_output_of_renderer_to_file(self):
        self.exporter.exportSingle(self.img)
        self.filesys.open.assert_called_with('provenance.html','w')
        self.filehandle.write.assert_called_with(self.template.render())

    def test_ExportList_uses_list_template(self):
        self.exporter.exportList([])
        self.templateLookup.get_template.assert_called_with('list.mako')

    def test_Export_uses_single_template(self):
        self.exporter.exportSingle(self.img)
        self.templateLookup.get_template.assert_called_with('single.mako')

    def test_Opens_file_created_with_firefox(self):
        self.exporter.exportList([])
        self.externals.run.assert_any_call(['firefox',
            'provenance.html'])

    def setupFilesys(self):
        filesys = Mock()
        filehandle = Mock()
        filehandle.__exit__ = lambda x,y,z,a : x
        filehandle.__enter__ = lambda x : x
        filesys.open.return_value = filehandle
        return (filesys, filehandle)




