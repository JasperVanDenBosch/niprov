

class DictFormat(object):

    def __init__(self, dependencies):
        pass

    def serialize(self, itemOrList):
        if isinstance(itemOrList, list):
            return [item.provenance for item in itemOrList]
        else:
            return itemOrList.provenance


