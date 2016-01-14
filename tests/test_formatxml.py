from tests.ditest import DependencyInjectionTestBase
from mock import Mock
import datetime


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

    def test_has_namespaces(self):
        from niprov.formatxml import XmlFormat
        form = XmlFormat(self.dependencies)
        out = form.serializeSingle(self.aFile())
        prov = 'http://www.w3.org/ns/prov#'
        self.assertNamespaceDefined('prov', prov, out)
        nfo = 'http://www.semanticdesktop.org/ontologies/2007/03/22/nfo#'
        self.assertNamespaceDefined('nfo', nfo, out)
        dct = 'http://purl.org/dc/terms/'
        self.assertNamespaceDefined('dct', dct, out)

    def test_Entity_has_id(self):
        from niprov.formatxml import XmlFormat
        form = XmlFormat(self.dependencies)
        aFile = self.aFile()
        doc = self.parseDoc(form.serializeSingle(aFile))
        entity = doc.getElementsByTagName("prov:entity")[0]
        self.assertHasAttributeWithValue(entity, 'id', 'niprov:file0')

    def test_serialize_file_entity_has_fileUrl_prop(self):
        from niprov.formatxml import XmlFormat
        form = XmlFormat(self.dependencies)
        aFile = self.aFile()
        doc = self.parseDoc(form.serializeSingle(aFile))
        entity = doc.getElementsByTagName("prov:entity")[0]
        self.assertOneChildWithTagAndText(entity, 'nfo:fileUrl', 
            str(aFile.location.toUrl()))

    def test_serialize_file_entity_has_fileSize_prop(self):
        from niprov.formatxml import XmlFormat
        form = XmlFormat(self.dependencies)
        aFile = self.aFile()
        aFile.provenance['size'] = 56789
        doc = self.parseDoc(form.serializeSingle(aFile))
        entity = doc.getElementsByTagName("prov:entity")[0]
        self.assertOneChildWithTagAndText(entity, 'nfo:fileSize', str(56789))

    def test_serialize_file_entity_has_fileLastModified_prop(self):
        from niprov.formatxml import XmlFormat
        form = XmlFormat(self.dependencies)
        aFile = self.aFile()
        aFile.provenance['created'] = datetime.datetime.now()
        doc = self.parseDoc(form.serializeSingle(aFile))
        entity = doc.getElementsByTagName("prov:entity")[0]
        self.assertOneChildWithTagAndText(entity, 'nfo:fileLastModified', 
            aFile.provenance['created'].isoformat())

    def test_serialize_file_entity_has_hash(self):
        from niprov.formatxml import XmlFormat
        form = XmlFormat(self.dependencies)
        aFile = self.aFile()
        aFile.provenance['hash'] = 'abraca777'
        doc = self.parseDoc(form.serializeSingle(aFile))
        entity = doc.getElementsByTagName("prov:entity")[0]
        hasHash = self.assertOneChildWithTagName(entity, 'nfo:hasHash')
        hashref = self.getElementContent(hasHash)
        allHashes = doc.getElementsByTagName("nfo:FileHash")
        hashesWithId = [e for e in allHashes if e.attributes['id'].value==hashref]
        self.assertEqual(1, len(hashesWithId))
        hashEl = hashesWithId[0]
        self.assertOneChildWithTagAndText(hashEl, 'nfo:hashAlgorithm', 'MD5')
        self.assertOneChildWithTagAndText(hashEl, 'nfo:hashValue', 
            aFile.provenance['hash'])

    def test_FileHash_id_follows_sensible_format(self):
        from niprov.formatxml import XmlFormat
        form = XmlFormat(self.dependencies)
        aFile = self.aFile()
        aFile.provenance['hash'] = 'abraca777'
        doc = self.parseDoc(form.serializeSingle(aFile))
        entity = doc.getElementsByTagName("prov:entity")[0]
        fileId = entity.attributes['id'].value
        self.assertOneChildWithTagAndText(entity, 'nfo:hasHash', fileId+'.hash')

    def test_file_with_transformation_has_activity_w_corresponding_id(self):
        from niprov.formatxml import XmlFormat
        form = XmlFormat(self.dependencies)
        aFile = self.aFile()
        aFile.provenance['transformation'] = 'enchantment'
        doc = self.parseDoc(form.serializeSingle(aFile))
        ent, entId = self.assertOneChildWithTagThatHasAnId(doc, 'prov:entity')
        act, actId = self.assertOneChildWithTagThatHasAnId(doc, 'prov:activity')
        self.assertEqual(entId+'.xform', actId)

    def test_file_with_transformation_has_activity_w_label(self):
        from niprov.formatxml import XmlFormat
        form = XmlFormat(self.dependencies)
        aFile = self.aFile()
        aFile.provenance['transformation'] = 'enchantment'
        doc = self.parseDoc(form.serializeSingle(aFile))
        entity = doc.getElementsByTagName("prov:entity")[0]
        activity = doc.getElementsByTagName("prov:activity")[0]
        self.assertOneChildWithTagAndText(activity, 'dct:title', 'enchantment')

    def test_file_with_transformation_has_wasGeneratedBy_element(self):
        from niprov.formatxml import XmlFormat
        form = XmlFormat(self.dependencies)
        aFile = self.aFile()
        aFile.provenance['transformation'] = 'enchantment'
        doc = self.parseDoc(form.serializeSingle(aFile))
        ent, entId = self.assertOneChildWithTagThatHasAnId(doc, 'prov:entity')
        act, actId = self.assertOneChildWithTagThatHasAnId(doc, 'prov:activity')
        wasGen = self.assertOneChildWithTagName(doc, "prov:wasGeneratedBy")
        refEnt = self.assertOneChildWithTagName(wasGen, "prov:entity")
        refAct = self.assertOneChildWithTagName(wasGen, "prov:activity")
        self.assertHasAttributeWithValue(refEnt, 'prov:ref', entId)
        self.assertHasAttributeWithValue(refAct, 'prov:ref', actId)

    def test_file_with_transformation_has_wasGeneratedBy_with_time(self):
        from niprov.formatxml import XmlFormat
        form = XmlFormat(self.dependencies)
        aFile = self.aFile()
        aFile.provenance['transformation'] = 'enchantment'
        aFile.provenance['created'] = datetime.datetime.now()
        doc = self.parseDoc(form.serializeSingle(aFile))
        wasGen = self.assertOneChildWithTagName(doc, "prov:wasGeneratedBy")
        self.assertOneChildWithTagAndText(wasGen, 'prov:time', 
            aFile.provenance['created'].isoformat())

    def parseDoc(self, xmlString):
        from xml.dom.minidom import parseString
        dom = parseString(xmlString)
        return dom.documentElement

    def assertNamespaceDefined(self, prefix, ns, xmlString):
        doc = self.parseDoc(xmlString)
        self.assertHasAttributeWithValue(doc, 'xmlns:'+prefix, ns)
        
    def assertHasAttributeWithValue(self, element, attName, attValue):
        assert element.hasAttribute(attName), "Can't find attribute: "+attName
        self.assertEqual(attValue, element.attributes[attName].value)

    def assertOneChildWithTagThatHasAnId(self, parent, tag):
        elements = parent.getElementsByTagName(tag)
        elements = [e for e in elements if e.hasAttribute('id')]
        msg = 'Expected exactly one {0} with ID in {1}, but found {2}'
        nElem = len(elements)
        self.assertEqual(1, nElem, msg.format(tag, parent.tagName, nElem))
        return elements[0], elements[0].attributes['id'].value

    def assertOneChildWithTagName(self, parent, tag):
        elements = parent.getElementsByTagName(tag)
        msg = 'Expected exactly one {0} in {1}, but found {2}'
        nElem = len(elements)
        self.assertEqual(1, nElem, msg.format(tag, parent.tagName, nElem))
        return elements[0]

    def assertOneChildWithTagAndText(self, parent, tag, expValue):
        elem = self.assertOneChildWithTagName(parent, tag)
        self.assertEqual(expValue, self.getElementContent(elem))

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
