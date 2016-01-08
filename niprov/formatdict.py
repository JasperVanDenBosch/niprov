from niprov.format import Format


class DictFormat(Format):

    def __init__(self, dependencies):
        pass

    def serialize(self, itemOrList):
        if isinstance(itemOrList, list):
            return [item.provenance for item in itemOrList]
        else:
            return itemOrList.provenance


