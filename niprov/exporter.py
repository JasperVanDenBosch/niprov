

class BaseExporter(object):
    """Parent Exporter class from which exporters for specific mediums are 
    derived.
    """

    def export(self, provenance):
        """Publish provenance.

        This determines if the provenance is for a single file or multiple,
        and then calls the appropriate more specific export method.
        """
        if isinstance(provenance, list):
            return self.exportList(provenance)
        else:
            return self.exportSingle(provenance)
