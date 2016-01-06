from xml.dom.minidom import Document
## Decided not to go with prov python lib as it depends on lxml which depends on c binaries


class XmlFormat(object):

    def __init__(self, dependencies):
        pass

    def serialize(self, itemOrList):
        if not isinstance(itemOrList, list):
            itemOrList = [itemOrList]
        ns = 'http://www.w3.org/ns/prov#'
        dom = Document()
        doc = self._createElementNS(dom, ns, 'prov', 'prov:document')
        dom.appendChild(doc)
        for item in itemOrList:
            entity = dom.createElementNS(ns, 'prov:entity')
            doc.appendChild(entity)
        return dom.toprettyxml(encoding="UTF-8")

    def _createElementNS(self, dom, ns, prefix, tag):
        element = dom.createElementNS(ns, tag)
        element.setAttribute('xmlns:'+prefix, ns)
        return element

