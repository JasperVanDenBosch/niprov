#!/usr/bin/python
# -*- coding: UTF-8 -*-
from __future__ import print_function
from niprov.exceptions import UnknownFileError
from niprov.dependencies import Dependencies


class Commandline(object):

    vlevels = ['debug','info','warning','error']

    def __init__(self, dependencies=Dependencies()):
        self.config = dependencies.config
        self.verbosity = dependencies.config.verbosity
        assert self.verbosity in self.vlevels, "Unknown verbosity value"

    def usingCopyAsParent(self, copy):
        loc = str(copy.location)
        self.log('warning', 'Used provenance from copy found at '+loc)

    def fileAdded(self, image):
        if image.status == 'new':
            self.log('info', 'New file: {0}'.format(image.path))
        if image.status == 'series-new-file':
            template = 'Added {0} file to series: {1}'
            nfiles = len(image.provenance['filesInSeries'])
            self.log('info', template.format(ordinal(nfiles), image.getSeriesId()))
        if image.status == 'new-version':
            self.log('info', 'Added new version for: {}'.format(image.path))

    def missingDependencyForImage(self, lib, fpath):
        template = 'Missing python package "{0}" to read file: {1}'        
        self.log('warning', template.format(lib, fpath))

    def fileError(self, fpath):
        import traceback
        traceback.print_exc()
        self.log('warning', 'Error inspecting file: {0}'.format(fpath))

    def interpretedRecording(self, new, transform, parents):
        template = ('[provenance] Recorded the command [{1}] to create [{0}] '+
            'based on [{2}]')
        self.log('info', template.format(', '.join(new), transform, 
            ', '.join(parents)))

    def renamedDicom(self, fpath):
        self.log('info', 'Renamed dicom file: '+fpath)

    def discoveryFinished(self, nnew, nadded, nfailed, ntotal):
        self.log('info', 'Discovered {0} new, added {1} to series, failed to read {2}, '
           'processed {3} total files.'.format(nnew, nadded, nfailed, ntotal))

    def mnefunEventReceived(self, operationName):
        self.log('info', 'Mnefun operation: '+operationName)

    def receivedBashCommand(self, command):
        self.log('info', 'Recording command: \n'+(' '.join(command)))

    def filesMarkedForApproval(self, images):
        paths = '\n'.join([img.path for img in images])
        self.log('info', 'Files marked for approval: \n{0}'.format(paths))

    def exportedToFile(self, fname):
        self.log('info', 'Exported to file: {0}'.format(fname))

    def log(self, level, message, exceptionClass=None):
        if self.vlevels.index(level) >= self.vlevels.index(self.verbosity):
            if level == 'error':
                if exceptionClass is None:
                    raise NiprovError(message)
                else:
                    raise exceptionClass(message)
            else:
                print('[provenance:{0}] {1}'.format(level, message))

    def addUnknownParent(self, fpath):
        self.log('warning', '{0} unknown. Adding to provenance'.format(fpath))
        

SUFFIXES = {1: 'st', 2: 'nd', 3: 'rd'}
def ordinal(num):
    if 10 <= num % 100 <= 20:
        suffix = 'th'
    else:
        # the second parameter is a default.
        suffix = SUFFIXES.get(num % 10, 'th')
    return str(num) + suffix

