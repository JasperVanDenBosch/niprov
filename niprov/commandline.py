#!/usr/bin/python
# -*- coding: UTF-8 -*-


class Commandline(object):

    def __init__(self, settings=None):
        self.settings = settings

    def fileFound(self, image):
        template = '[provenance] {0}'
        print(template.format(image.path))

    def fileFoundInSeries(self, img, series):
        template = '[provenance] Adding {0} file to series: {1}'
        nfiles = len(series.provenance['filesInSeries'])
        print(template.format(ordinal(nfiles), series.getSeriesId()))

    def missingDependencyForImage(self, lib, fpath):
        template = '[provenance] Missing python package "{0}" to read file: {1}'        
        print(template.format(lib, fpath))

    def fileError(self, fpath):
        import traceback
        traceback.print_exc()
        print('[provenance] Error inspecting file: {0}'.format(fpath))

    def interpretedRecording(self, new, transform, parents):
        template = ('[provenance] Recorded the command [{1}] to create [{0}] '+
            'based on [{2}]')
        print(template.format(', '.join(new), transform, ', '.join(parents)))

    def unknownFile(self, fpath):
        print('[provenance] Unknown file: '+fpath)

    def knownFile(self, fpath):
        print('[provenance] File already known: '+fpath)

    def renamedDicom(self, fpath):
        print('[provenance] Renamed dicom file: '+fpath)

    def discoveryFinished(self, nnew, nadded, nfailed, ntotal):
        print('[provenance] Discovered {0} new, added {1} to series, failed to read {2}, '
           'processed {3} total files.'.format(nnew, nadded, nfailed, ntotal))

    def mnefunEventReceived(self, operationName):
        print('[provenance] Mnefun operation: '+operationName)

    def receivedBashCommand(self, command):
        print('[provenance] Recording command: \n'+(' '.join(command)))

    def filesMarkedForApproval(self, images):
        print('[provenance] Files marked for approval:')
        for img in images:
            print(img.path)

SUFFIXES = {1: 'st', 2: 'nd', 3: 'rd'}
def ordinal(num):
    if 10 <= num % 100 <= 20:
        suffix = 'th'
    else:
        # the second parameter is a default.
        suffix = SUFFIXES.get(num % 10, 'th')
    return str(num) + suffix

