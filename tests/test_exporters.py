import unittest
from mock import Mock

class ExportFactoryTests(unittest.TestCase):

    def test_Html(self):
        from niprov.exporters import ExportFactory
        from niprov.html import HtmlExporter
        exporter = ExportFactory().createExporter('html', None)
        self.assertIsInstance(exporter, HtmlExporter)

    def test_Default(self):
        from niprov.exporters import ExportFactory
        from niprov.directexporter import DirectExporter
        exporter = ExportFactory().createExporter(None, None)
        self.assertIsInstance(exporter, DirectExporter)

    def test_StdOut(self):
        from niprov.exporters import ExportFactory
        from niprov.stdout import StandardOutputExporter
        exporter = ExportFactory().createExporter('stdout', None)
        self.assertIsInstance(exporter, StandardOutputExporter)

    def test_Form_supplied(self):
        from niprov.exporters import ExportFactory
        exporter = ExportFactory().createExporter(None, 'narrative')
        self.assertEqual(exporter.form, 'narrative')
        exporter = ExportFactory().createExporter('html', None)
        self.assertEqual(exporter.form, None)
        exporter = ExportFactory().createExporter('stdout', 'narrative')
        self.assertEqual(exporter.form, 'narrative')




