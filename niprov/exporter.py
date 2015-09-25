from niprov.dependencies import Dependencies


class BaseExporter(object):
    """Parent Exporter class from which exporters for specific mediums are 
    derived.
    """

    def __init__(self, form=None, dependencies=Dependencies()):
        self.form = form
        self.narrator = dependencies.getNarrator()

    def export(self, provenance):
        """Publish provenance.

        This determines if the provenance is for a single file or multiple,
        and then calls the appropriate more specific export method.
        """
        if self.form == 'narrative':
            return self.exportNarrative(provenance)
        elif isinstance(provenance, list):
            return self.exportList(provenance)
        elif isinstance(provenance, dict):
            return self.exportStatistics(provenance)
        else:
            return self.exportSingle(provenance)

    def exportList(self, provenance):
        raise NotImplementedError('exportList')

    def exportSingle(self, provenance):
        raise NotImplementedError('exportSingle')

    def exportNarrative(self, provenance):
        raise NotImplementedError('exportNarrative')

    def exportStatistics(self, provenance):
        raise NotImplementedError('exportStatistics')
