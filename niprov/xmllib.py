from xml.dom.minidom import parse

def getNonTextChildNodes(node):
    return [n for n in node.childNodes if n.nodeType != n.TEXT_NODE]

def getElementsByTagNameWithoutPrefix(node, partialTagName):
    childNodes = getNonTextChildNodes(node)
    tagLength = len(partialTagName)
    matchingNodes = []
    for childNode in childNodes:
        if len(childNode.tagName) >= tagLength:
            if childNode.tagName[-tagLength:] == partialTagName:
                matchingNodes.append(childNode)
    return matchingNodes

def getTextContent(node):
    textChildNodes = [n for n in node.childNodes if n.nodeType == n.TEXT_NODE]
    return ''.join([n.data for n in textChildNodes])

def getTextContentForFirstElementByTag(node, tagname):
    firstChildByTag = node.getElementsByTagName(tagname)[0]
    return getTextContent(firstChildByTag)

def getRefForFirstElementByTag(node, tagname):
    firstChildByTag = node.getElementsByTagName(tagname)[0]
    href = firstChildByTag.getAttribute('href')
    return href[1:]

def getElementById(node, targetId):
    for childNode in node.childNodes:
        if childNode.nodeType != childNode.TEXT_NODE:
            if childNode.hasAttribute('id'):
                idval = childNode.getAttribute('id')
                if idval == targetId:
                    return childNode
    raise ValueError('Cannot find element with id')
