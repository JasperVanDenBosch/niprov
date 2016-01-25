from xml.dom.minidom import Document
from niprov.format import Format
## Decided not to go with prov python lib as it depends on lxml which depends on c binaries


class XmlFormat(Format):

    def __init__(self, dependencies):
        super(XmlFormat, self).__init__(dependencies)
        self.fileExtension = 'xml'

    def serializeSingle(self, item):
        return self.serializeList([item])

    def serializeList(self, itemOrList):
        prov = 'http://www.w3.org/ns/prov#'
        nfo = 'http://www.semanticdesktop.org/ontologies/2007/03/22/nfo#'
        dct = 'http://purl.org/dc/terms/'
        dom = Document()
        doc = dom.createElementNS(prov, 'prov:document')
        doc.setAttribute('xmlns:prov', prov)
        doc.setAttribute('xmlns:nfo', nfo)
        doc.setAttribute('xmlns:dct', dct)
        dom.appendChild(doc)
        for i, item in enumerate(itemOrList):
            entity = dom.createElementNS(prov, 'prov:entity')
            entityId = 'niprov:file'+str(i)
            entity.setAttribute('id', entityId)

            fileUrl = dom.createElementNS(nfo, 'nfo:fileUrl')
            fileUrlVal = dom.createTextNode(item.location.toUrl())
            fileUrl.appendChild(fileUrlVal)
            entity.appendChild(fileUrl)

            if 'size' in item.provenance:

                fileSize = dom.createElementNS(nfo, 'nfo:fileSize')
                fileSizeVal = dom.createTextNode(str(item.provenance['size']))
                fileSize.appendChild(fileSizeVal)
                entity.appendChild(fileSize)

            if 'created' in item.provenance:

                fileLastMod = dom.createElementNS(nfo, 'nfo:fileLastModified')
                fileLastModVal = dom.createTextNode(item.provenance['created'].isoformat())
                fileLastMod.appendChild(fileLastModVal)
                entity.appendChild(fileLastMod)

            if 'hash' in item.provenance:

                fileHash = dom.createElementNS(nfo, 'nfo:FileHash')
                hashId = entityId+'.hash'
                fileHash.setAttribute('id', hashId)

                hashAlgo = dom.createElementNS(nfo, 'nfo:hashAlgorithm')
                hashAlgoVal = dom.createTextNode('MD5')
                hashAlgo.appendChild(hashAlgoVal)
                fileHash.appendChild(hashAlgo)

                hashValue = dom.createElementNS(nfo, 'nfo:hashValue')
                hashValueVal = dom.createTextNode(item.provenance['hash'])
                hashValue.appendChild(hashValueVal)
                fileHash.appendChild(hashValue)

                hasHash = dom.createElementNS(nfo, 'nfo:hasHash')
                hasHashVal = dom.createTextNode(hashId)
                hasHash.appendChild(hasHashVal)
                entity.appendChild(hasHash)

                doc.appendChild(fileHash)

            if 'transformation' in item.provenance:

                act = dom.createElementNS(prov, 'prov:activity')
                activityId = entityId+'.xform'
                act.setAttribute('id', activityId)

                actTitle = dom.createElementNS(dct, 'dct:title')
                actTitleVal = dom.createTextNode(item.provenance['transformation'])
                actTitle.appendChild(actTitleVal)
                act.appendChild(actTitle)
                doc.appendChild(act)

                wasGen = dom.createElementNS(prov, 'prov:wasGeneratedBy')
                entityRef = dom.createElementNS(prov, 'prov:entity')
                entityRef.setAttribute('prov:ref', entityId)
                wasGen.appendChild(entityRef)
                activityRef = dom.createElementNS(prov, 'prov:activity')
                activityRef.setAttribute('prov:ref', activityId)
                wasGen.appendChild(activityRef)
                doc.appendChild(wasGen)

                if 'created' in item.provenance:
                    wasGenTime = dom.createElementNS(prov, 'prov:time')
                    wasGenTimeVal = dom.createTextNode(item.provenance['created'].isoformat())
                    wasGenTime.appendChild(wasGenTimeVal)
                    wasGen.appendChild(wasGenTime)

            doc.appendChild(entity)

        return dom.toprettyxml(encoding="UTF-8")


