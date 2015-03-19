import unittest
from mock import Mock

class ExportFactoryTests(unittest.TestCase):

    def test_Html(self):
        from niprov.exporters import ExportFactory
        from niprov.html import HtmlExporter
        exporter = ExportFactory().createExporter('html')
        self.assertIsInstance(exporter, HtmlExporter)

    def test_Default(self):
        from niprov.exporters import ExportFactory
        from niprov.directexporter import DirectExporter
        exporter = ExportFactory().createExporter(None)
        self.assertIsInstance(exporter, DirectExporter)

    def test_StdOut(self):
        from niprov.exporters import ExportFactory
        from niprov.stdout import StandardOutputExporter
        exporter = ExportFactory().createExporter('stdout')
        self.assertIsInstance(exporter, StandardOutputExporter)




