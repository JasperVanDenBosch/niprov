#!/usr/bin/python
# -*- coding: UTF-8 -*-
from niprov.exporter import BaseExporter


class DirectExporter(BaseExporter):
    """Dummy  Exporter class which simply returns the provenance passed.
    """

    def exportList(self, provenance):
        return provenance

    def exportSingle(self, provenance):
        return provenance

    def exportNarrative(self, provenance):
        return self.narrator.narrate(provenance)

    def exportStatistics(self, stats):
        return stats
