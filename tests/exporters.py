import unittest
from mock import Mock

class ExportFactoryTests(unittest.TestCase):

    def test_Html(self):
        from niprov.exporters import ExportFactory
        from niprov.html import HtmlExporter
        exporter = ExportFactory().createExporter('html')
        self.assertIsInstance(exporter, HtmlExporter)




