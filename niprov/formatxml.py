from xml.dom.minidom import Document
from niprov.format import Format
## Decided not to go with prov python lib as it depends on lxml which depends on c binaries


class XmlFormat(Format):

    def serializeSingle(self, item):
        return self.serializeList([item])

    def serializeList(self, itemOrList):
        prov = 'http://www.w3.org/ns/prov#'
        nfo = 'http://www.semanticdesktop.org/ontologies/2007/03/22/nfo#'
        dom = Document()
        doc = dom.createElementNS(prov, 'prov:document')
        doc.setAttribute('xmlns:prov', prov)
        doc.setAttribute('xmlns:nfo', nfo)
        dom.appendChild(doc)
        for item in itemOrList:
            entity = dom.createElementNS(prov, 'prov:entity')

            fileUrl = dom.createElementNS(nfo, 'nfo:fileUrl')
            fileUrlVal = dom.createTextNode(item.location.toUrl())
            fileUrl.appendChild(fileUrlVal)
            entity.appendChild(fileUrl)

            fileSize = dom.createElementNS(nfo, 'nfo:fileSize')
            fileSizeVal = dom.createTextNode(str(item.provenance['size']))
            fileSize.appendChild(fileSizeVal)
            entity.appendChild(fileSize)

            fileLastMod = dom.createElementNS(nfo, 'nfo:fileLastModified')
            fileLastModVal = dom.createTextNode(item.provenance['created'].isoformat())
            fileLastMod.appendChild(fileLastModVal)
            entity.appendChild(fileLastMod)

            doc.appendChild(entity)
        return dom.toprettyxml(encoding="UTF-8")


