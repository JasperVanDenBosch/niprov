from niprov.format import Format


class DictFormat(Format):

    def serializeSingle(self, item):
        return item.provenance

    def serializeList(self, fileList):
        return [item.provenance for item in fileList]


