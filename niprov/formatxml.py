import xml.etree.ElementTree as xml
import StringIO
## Decided not to go with prov python lib as it depends on lxml which depends on c binaries


class XmlFormat(object):

    def export(self, fileObject):
        outstr = StringIO.StringIO()
        a = xml.Element('prov:abc')
        tree = xml.ElementTree(a)
        tree.write(outstr, encoding='UTF-8', xml_declaration=True)
        return outstr.getvalue()
