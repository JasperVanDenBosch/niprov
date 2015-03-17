#!/usr/bin/python
# -*- coding: UTF-8 -*-
import copy


class StandardOutputExporter(object):

    _expectedFields = ['acquired','subject','protocol','dimensions','path']

    def exportList(self, provenance):
        """Publish the provenance for several images on the commandline.

        Args:
            provenance (list): List of provenance dictionaries.
        """
        print('\n')
        print('{0:20} {1:12} {2:24} {3:20} {4:24}'.format(*self._expectedFields))
        for record in provenance:
            self.exportSummary(record)
        print('\n')

    def export(self, provenance):
        """Publish the provenance for one image on the commandline.

        Args:
            provenance (dict): Provenance for one image file
        """
        print('\n')
        for field, value in provenance.items():
            print('{0:24} {1}'.format(field+':', str(value)))
        print('\n')

    def exportSummary(self, provenance):
        """Publish a summary of the provenance for one image as one line in 
        the terminal.

        Args:
            provenance (dict): Provenance for one image file
        """
        provcopy = copy.deepcopy(provenance)
        for field in self._expectedFields:
            if field not in provcopy:
                provcopy[field] = None
        tmp = ('{0[acquired]!s}  {0[subject]!s:12} {0[protocol]!s:24} '
            '{0[dimensions]!s:20} {0[path]!s:24}')
        print(tmp.format(provcopy))
