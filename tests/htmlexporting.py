import unittest
from mock import Mock

class HtmlTests(unittest.TestCase):

    def test_Without_specifics_returns_all_files(self):
        from niprov.html import HtmlExporter
        log = Mock()
        html = HtmlExporter()
        item1 = Mock()
        item2 = Mock()
        html.exportList([item1, item2])




