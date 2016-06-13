from niprov.dependencies import Dependencies
from niprov.basefile import BaseFile
from niprov.pipeline import Pipeline


class Format(object):
    """Parent Format class from which specific formats are derived.
    """

    def __init__(self, dependencies=Dependencies()):
        self.fileExtension = 'txt'

    def serialize(self, provenance):
        """Publish provenance.

        This determines if the provenance is for a single file or multiple,
        and then calls the appropriate more specific serialize method.
        """
        if isinstance(provenance, Pipeline):
            return self.serializePipeline(provenance)
        elif isinstance(provenance, dict):
            return self.serializeStatistics(provenance)
        elif hasattr(provenance, '__iter__'):
            return self.serializeList(provenance)
        else:
            return self.serializeSingle(provenance)

    def serializeList(self, provenance):
        raise NotImplementedError('serializeList')

    def serializeSingle(self, provenance):
        raise NotImplementedError('serializeSingle')

    def serializeStatistics(self, provenance):
        raise NotImplementedError('serializeStatistics')

    def serializePipeline(self, pipeline):
        raise NotImplementedError('serializePipeline')
