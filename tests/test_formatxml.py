from tests.ditest import DependencyInjectionTestBase
from mock import Mock


class XmlFormatTests(DependencyInjectionTestBase):

    def setUp(self):
        super(XmlFormatTests, self).setUp()

    def test_serialize_item_returns_string_with_xml_header(self):
        prolog = '<?xml version="1.0" encoding="UTF-8"?>'
        doc = '<prov:document xmlns:prov="http://www.w3.org/ns/prov#">'
        from niprov.formatxml import XmlFormat
        form = XmlFormat(self.dependencies)
        out = form.serialize(self.aFile())
        self.assertIn(prolog, out)
        self.assertIn(doc, out)

    def test_serialize_list_creates_entity_for_each_file(self):
        from niprov.formatxml import XmlFormat
        form = XmlFormat(self.dependencies)
        out = form.serialize([self.aFile(), self.aFile(), self.aFile()])
        self.assertEqual(3, out.count('prov:entity'))

    def aFile(self):
        somefile = Mock()
        somefile.provenance = {}
        return somefile
