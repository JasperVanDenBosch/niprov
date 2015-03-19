from niprov.narrator import Narrator


class BaseExporter(object):
    """Parent Exporter class from which exporters for specific mediums are 
    derived.
    """

    def __init__(self, form=None, narrator=Narrator()):
        self.form = form
        self.narrator = narrator

    def export(self, provenance):
        """Publish provenance.

        This determines if the provenance is for a single file or multiple,
        and then calls the appropriate more specific export method.
        """
        if self.form == 'narrative':
            return self.exportNarrative(provenance)
        elif isinstance(provenance, list):
            return self.exportList(provenance)
        else:
            return self.exportSingle(provenance)

    def exportList(self, provenance):
        raise NotImplementedError('exportList')

    def exportSingle(self, provenance):
        raise NotImplementedError('exportSingle')

    def exportNarrative(self, provenance):
        raise NotImplementedError('exportNarrative')
