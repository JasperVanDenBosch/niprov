from tests.ditest import DependencyInjectionTestBase
from mock import Mock


class XmlFormatTests(DependencyInjectionTestBase):

    def setUp(self):
        super(XmlFormatTests, self).setUp()

    def test_serialize_item_returns_string_with_xml_header(self):
        prolog = '<?xml version="1.0" encoding="UTF-8"?>'
        doc = '<prov:document'
        from niprov.formatxml import XmlFormat
        form = XmlFormat(self.dependencies)
        out = form.serializeSingle(self.aFile())
        self.assertIn(prolog, out)
        self.assertIn(doc, out)

    def test_serialize_list_creates_entity_for_each_file(self):
        from niprov.formatxml import XmlFormat
        form = XmlFormat(self.dependencies)
        out = form.serializeList([self.aFile(), self.aFile(), self.aFile()])
        self.assertEqual(3, out.count('<prov:entity'))

    def test_has_PROV_namespace(self):
        from niprov.formatxml import XmlFormat
        form = XmlFormat(self.dependencies)
        out = form.serializeSingle(self.aFile())
        docline = [l for l in out.split('\n') if 'prov:doc' in l][0]
        prov = 'http://www.w3.org/ns/prov#'
        nsattr = 'xmlns:prov="{0}"'.format(prov)
        self.assertIn(nsattr, docline)

    def test_has_NFO_namespace(self):
        from niprov.formatxml import XmlFormat
        form = XmlFormat(self.dependencies)
        out = form.serializeSingle(self.aFile())
        docline = [l for l in out.split('\n') if 'prov:doc' in l][0]
        nfo = 'http://www.semanticdesktop.org/ontologies/2007/03/22/nfo#'
        nsattr = 'xmlns:nfo="{0}"'.format(nfo)
        self.assertIn(nsattr, docline)

    def test_serialize_file_entity_has_fileUrl_prop(self):
        from niprov.formatxml import XmlFormat
        form = XmlFormat(self.dependencies)
        aFile = self.aFile()
        out = form.serializeSingle(aFile)
        from xml.dom.minidom import parseString
        dom = parseString(out)
        entity = dom.getElementsByTagName("prov:entity")[0]
        targetPropElements = entity.getElementsByTagName("nfo:fileUrl")
        self.assertEqual(1, len(targetPropElements))
        self.assertEqual(str(aFile.location.toUrl()), 
            self.getElementContent(targetPropElements[0]))

    def getElementContent(self, element):
        rc = []
        for node in element.childNodes:
            if node.nodeType == node.TEXT_NODE:
                rc.append(node.data)
        return ''.join(rc)

    def aFile(self):
        somefile = Mock()
        somefile.provenance = {}
        somefile.location.toUrl.return_value = 'xkcd://HAL/location.loc'
        return somefile
