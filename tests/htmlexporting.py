import unittest
from mock import Mock
from datetime import datetime
import os

class HtmlTests(unittest.TestCase):


#    def test_Shortens_path_to_max_30chars(self):
#        from niprov.html import HtmlExporter
#        log = Mock()
#        externals = Mock()
#        (filesys, filehandle) = self.setupFilesys()
#        html = HtmlExporter(filesys, log, externals)
#        item1 = {}
#        item1['path'] = '12345678901234567890123456789012345678901234567890'
#        html.exportList([item1])
#        self.assertEqual('..1234567890123456789012345678901234567890')

    def setUp(self):
        import niprov.html
        self.log = Mock()
        self.externals = Mock()
        self.template = Mock()
        self.templateLookup = Mock()
        self.templateLookup.get_template.return_value = self.template
        niprov.html.TemplateLookup = Mock()
        niprov.html.TemplateLookup.return_value = self.templateLookup
        (self.filesys, self.filehandle) = self.setupFilesys()
        self.exporter = niprov.html.HtmlExporter(self.filesys, self.log, self.externals)

    def test_Writes_output_of_renderer_to_file(self):
        self.exporter.exportList([])
        self.filesys.open.assert_called_with('provenance.html','w')
        self.filehandle.write.assert_called_with(self.template.render())

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




