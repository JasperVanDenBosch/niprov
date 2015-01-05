import unittest
from mock import Mock
from datetime import datetime

class HtmlTests(unittest.TestCase):

    def test_Writes_one_list_item_per_entry(self):
        from niprov.html import HtmlExporter
        log = Mock()
        filesys = Mock()
        filehandle = Mock()
        filehandle.__exit__ = lambda x,y,z,a : x
        filehandle.__enter__ = lambda x : x
        filesys.open.return_value = filehandle
        html = HtmlExporter(filesys, log)
        item1 = {}
        item1['subject'] = 'John'
        item1['protocol'] = 'DTI'
        item1['acquired'] = datetime(2014, 8, 5, 12, 23, 46)
        item2 = {}
        item2['subject'] = 'Jane'
        item2['protocol'] = 'T1'
        item2['acquired'] = datetime(2014, 8, 6, 12, 23, 46)
        html.exportList([item1, item2])
        filehandle.write.assert_any_call('<li>2014-08-05 12:23:46 John DTI</li>')
        filehandle.write.assert_any_call('<li>2014-08-06 12:23:46 Jane T1</li>')

#    def test_Reports_html_file_location_to_listener(self):
#        self.assertTrue(False)

#    def test_Opens_file_created_with_firefox(self):
#        self.assertTrue(False)




