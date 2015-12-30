from xml.dom.minidom import Document
## Decided not to go with prov python lib as it depends on lxml which depends on c binaries


class XmlFormat(object):

    def export(self, fileObject):
        provns = 'http://www.w3.org/ns/prov#'
        dom = Document()
        doc = dom.createElementNS(provns, 'prov:document')
        dom.appendChild(doc)
http://stackoverflow.com/questions/863774/how-to-generate-xml-documents-with-namespaces-in-python
        return dom.toprettyxml(encoding="UTF-8")

