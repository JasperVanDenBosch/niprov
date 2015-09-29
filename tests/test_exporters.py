import unittest
from mock import Mock

class ExportFactoryTests(unittest.TestCase):

    def setUp(self):
        self.dependencies = Mock()
        from niprov.exporters import ExportFactory
        self.factory = ExportFactory(dependencies=self.dependencies)

    def test_Default(self):
        from niprov.directexporter import DirectExporter
        exporter = self.factory.createExporter(None, None)
        self.assertIsInstance(exporter, DirectExporter)

    def test_StdOut(self):
        from niprov.stdout import StandardOutputExporter
        exporter = self.factory.createExporter('stdout', None)
        self.assertIsInstance(exporter, StandardOutputExporter)

    def test_Form_supplied(self):
        exporter = self.factory.createExporter(None, 'narrative')
        self.assertEqual(exporter.form, 'narrative')
        exporter = self.factory.createExporter('stdout', 'narrative')
        self.assertEqual(exporter.form, 'narrative')




