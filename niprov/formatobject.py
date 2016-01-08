from niprov.format import Format


class ObjectFormat(Format):

    def serializeSingle(self, provenance):
        return provenance

    def serializeList(self, provenance):
        return provenance

    def serializeStatistics(self, provenance):
        return provenance

    def serializePipeline(self, provenance):
        return provenance
