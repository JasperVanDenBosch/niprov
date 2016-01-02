import unittest
from mock import Mock


class XmlFormatTests(unittest.TestCase):

    def setUp(self):
        pass

    def test_export_item_returns_string_with_xml_header(self):
        prolog = '<?xml version="1.0" encoding="UTF-8"?>'
        doc = '<prov:document xmlns:prov="http://www.w3.org/ns/prov#">'
        from niprov.formatxml import XmlFormat
        form = XmlFormat()
        out = form.export(self.aFile())
        self.assertIn(prolog, out)
        self.assertIn(doc, out)

    def test_export_list_creates_entity_for_each_file(self):
        from niprov.formatxml import XmlFormat
        form = XmlFormat()
        out = form.export([self.aFile(), self.aFile(), self.aFile()])
        self.assertEqual(3, out.count('prov:entity'))

    def aFile(self):
        somefile = Mock()
        somefile.provenance = {}
        return somefile
