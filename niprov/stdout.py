#!/usr/bin/python
# -*- coding: UTF-8 -*-
from __future__ import print_function
import copy
from niprov.exporter import BaseExporter


class StandardOutputExporter(BaseExporter):

    _expectedFields = ['acquired','subject','protocol','dimensions','path']

    def exportList(self, images):
        """Publish the provenance for several images on the commandline.

        Args:
            provenance (list): List of provenance dictionaries.
        """
        print('\n')
        print('{0:20} {1:12} {2:24} {3:20} {4:24}'.format(*self._expectedFields))
        for image in images:
            self.exportSummary(image)
        print('\n')

    def exportSingle(self, img):
        """Publish the provenance for one image on the commandline.

        Args:
            provenance (dict): Provenance for one image file
        """
        print('\n')
        for field, value in img.provenance.items():
            print('{0:24} {1}'.format(field+':', str(value)))
        print('\n')

    def exportSummary(self, image):
        """Publish a summary of the provenance for one image as one line in 
        the terminal.

        Args:
            provenance (dict): Provenance for one image file
        """
        provcopy = copy.deepcopy(image.provenance)
        for field in self._expectedFields:
            if field not in provcopy:
                provcopy[field] = None
        tmp = ('{0[acquired]!s}  {0[subject]!s:12} {0[protocol]!s:24} '
            '{0[dimensions]!s:20} {0[path]!s:24}')
        print(tmp.format(provcopy))

    def exportNarrative(self, provenance):
        """Publish provenance in a 'story' format in the terminal.

        Args:
            provenance (dict or list): Provenance either for one file or several.
        """
        print('\n')
        print(self.narrator.narrate(provenance))
        print('\n')

    def exportStatistics(self, stats):
        """Publish statistics for collected provenance in the terminal.

        Args:
            stats (dict): Dictionary with summary values.
        """
        print('\n')
        print(' Number of files: {0}'.format(stats['count']))
        print(' Total file size: {0}'.format(stats['totalsize']))
        print('\n')
