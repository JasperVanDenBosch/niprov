from __future__ import print_function
import copy
from niprov.format import Format


class SimpleFormat(Format):

    _expectedFields = ['acquired','subject','protocol','dimensions','path']

    def serializeList(self, images):
        """Publish the provenance for several images on the commandline.

        Args:
            provenance (list): List of provenance dictionaries.
        """
        text = ''
        text += '\n'
        text += '{0:20} {1:12} {2:24} {3:20} {4:24}'.format(*self._expectedFields)
        for image in images:
            text += self.serializeSummary(image)
            text += '\n'
        text += '\n'
        return text

    def serializeSingle(self, img):
        """Publish the provenance for one image on the commandline.

        Args:
            provenance (dict): Provenance for one image file
        """
        text = ''
        text += '\n'
        for field, value in img.provenance.items():
            text += '{0:24} {1}\n'.format(field+':', str(value))
        text += '\n'
        return text

    def serializeSummary(self, image):
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
        return tmp.format(provcopy)

    def serializeStatistics(self, stats):
        """Publish statistics for collected provenance in the terminal.

        Args:
            stats (dict): Dictionary with summary values.
        """
        text = ''
        text += '\n'
        text += ' Number of files: {0}\n'.format(stats['count'])
        text += ' Total file size: {0}\n'.format(stats['totalsize'])
        text += '\n'
        return text

    def serializePipeline(self, pipeline):
        """Pretty-print a pipeline to the terminal

        Args:
            pipeline (Pipeline): Pipeline object to publish.
        """
        tree = pipeline.asFilenameTree()
        def prettyPrintTree(tree, s='', lvl=0):
            for key, value in tree.items():
                s += '{0}+---{1}\n'.format('|   '*lvl,key)
                s = prettyPrintTree(value, s, lvl+1)
            return s
        return prettyPrintTree(tree)

