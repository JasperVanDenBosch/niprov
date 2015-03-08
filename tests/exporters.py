import unittest
from mock import Mock

class ExportFactoryTests(unittest.TestCase):

    def test_Html(self):
        from niprov.exporters import ExportFactory
        from niprov.html import HtmlExporter
        exporter = ExportFactory().createExporter('html')
        self.assertIsInstance(exporter, HtmlExporter)

    def test_Default(self):
        from niprov.exporters import ExportFactory, DummyExporter
        exporter = ExportFactory().createExporter(None)
        self.assertIsInstance(exporter, DummyExporter)




