import unittest
from mock import Mock, sentinel

class BaseExporterTests(unittest.TestCase):

    def test_If_export_called_with_list_calls_exportList(self):
        from niprov.exporter import BaseExporter
        exp = BaseExporter()
        exp.exportList = Mock()
        out = exp.export([sentinel.p1, sentinel.p2])
        exp.exportList.assert_called_with([sentinel.p1, sentinel.p2])
        self.assertEqual(out, exp.exportList())

    def test_If_export_called_with_list_calls_exportSingle(self):
        from niprov.exporter import BaseExporter
        exp = BaseExporter()
        exp.exportSingle = Mock()
        out = exp.export(sentinel.p1)
        exp.exportSingle.assert_called_with(sentinel.p1)
        self.assertEqual(out, exp.exportSingle())



