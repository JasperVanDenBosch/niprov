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

    def fileFound(self, image):
        self.log('info', 'New file: {0}'.format(image.path))

    def fileFoundInSeries(self, img, series):
        template = 'Adding {0} file to series: {1}'
        nfiles = len(series.provenance['filesInSeries'])
        self.log('info', template.format(ordinal(nfiles), series.getSeriesId()))

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

    def unknownFile(self, fpath):
        if self.config.dryrun:
            level = 'info'
        else:
            level = 'error'
        self.log(level, 'Unknown file: '+fpath, UnknownFileError)

    def knownFile(self, fpath):
        self.log('info', 'File already known: '+fpath)

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

    def log(self, level, message, exceptionClass=None):
        if self.vlevels.index(level) >= self.vlevels.index(self.verbosity):
            if level == 'error':
                if exceptionClass is None:
                    raise NiprovError(message)
                else:
                    raise exceptionClass(message)
            else:
                print('[provenance:{0}] {1}'.format(level, message))
        

SUFFIXES = {1: 'st', 2: 'nd', 3: 'rd'}
def ordinal(num):
    if 10 <= num % 100 <= 20:
        suffix = 'th'
    else:
        # the second parameter is a default.
        suffix = SUFFIXES.get(num % 10, 'th')
    return str(num) + suffix

