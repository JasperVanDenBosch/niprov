import unittest
from mock import Mock
from datetime import datetime
import os

class HtmlTests(unittest.TestCase):

    def test_Writes_one_list_item_per_entry(self):
        from niprov.html import HtmlExporter
        log = Mock()
        externals = Mock()
        (filesys, filehandle) = self.setupFilesys()
        html = HtmlExporter(filesys, log, externals)
        item1 = {}
        item1['path'] = '/p/f1'
        item1['subject'] = 'John'
        item1['protocol'] = 'DTI'
        item1['acquired'] = datetime(2014, 8, 5, 12, 23, 46)
        item2 = {}
        item1['path'] = '/p/f2'
        item2['subject'] = 'Jane'
        item2['protocol'] = 'T1'
        item2['acquired'] = datetime(2014, 8, 6, 12, 23, 46)
        html.exportList([item1, item2])
        filehandle.write.assert_any_call('<li>2014-08-05 12:23:46 John DTI /p/f1</li>')
        filehandle.write.assert_any_call('<li>2014-08-06 12:23:46 Jane T1 /p/f2</li>')

    def test_If_item_misses_field_fills_questionmark(self):
        from niprov.html import HtmlExporter
        log = Mock()
        externals = Mock()
        (filesys, filehandle) = self.setupFilesys()
        html = HtmlExporter(filesys, log, externals)
        item1 = {}
        item1['path'] = '/p/f1'
        item1['protocol'] = 'DTI'
        item1['acquired'] = datetime(2014, 8, 5, 12, 23, 46)
        item2 = {}
        item2['path'] = '/p/f2'
        item2['subject'] = 'Jane'
        item2['protocol'] = 'T1'
        html.exportList([item1, item2])
        filehandle.write.assert_any_call('<li>2014-08-05 12:23:46 ? DTI /p/f1</li>')
        filehandle.write.assert_any_call('<li>? Jane T1 /p/f2</li>')

    def test_Shortens_path_to_max_30chars(self):
        from niprov.html import HtmlExporter
        log = Mock()
        externals = Mock()
        (filesys, filehandle) = self.setupFilesys()
        html = HtmlExporter(filesys, log, externals)
        item1 = {}
        item1['path'] = '12345678901234567890123456789012345678901234567890'
        html.exportList([item1])
        filehandle.write.assert_any_call('<li>? ? ? ..1234567890123456789012345678901234567890</li>')

    def test_Writes_one_list_item_per_entry(self):
        from niprov.html import HtmlExporter
        log = Mock()
        externals = Mock()
        (filesys, filehandle) = self.setupFilesys()
        html = HtmlExporter(filesys, log, externals)
        html.exportList([])
        filesys.open.assert_any_call('provenance.html','w')

#    def test_Reports_html_file_location_to_listener(self):
#        self.assertTrue(False)

    def test_Opens_file_created_with_firefox(self):
        from niprov.html import HtmlExporter
        log = Mock()
        externals = Mock()
        (filesys, filehandle) = self.setupFilesys()
        html = HtmlExporter(filesys, log, externals)
        html.exportList([])
        externals.run.assert_any_call(['firefox',
            'provenance.html'])

    def setupFilesys(self):
        filesys = Mock()
        filehandle = Mock()
        filehandle.__exit__ = lambda x,y,z,a : x
        filehandle.__enter__ = lambda x : x
        filesys.open.return_value = filehandle
        return (filesys, filehandle)




