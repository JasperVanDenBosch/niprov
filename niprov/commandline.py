#!/usr/bin/python
# -*- coding: UTF-8 -*-


class Commandline(object):

    def fileFound(self, fname, provenance):
        template = '[provenance] {0[path]}'
        print(template.format(provenance))

    def missingDependencyForImage(self, lib, fpath):
        template = '[provenance] Missing python package "{0}" to read file: {1}'        
        print(template.format(lib, fpath))

    def fileError(self, fpath):
        print('[provenance] Error opening file: {0}'.format(fpath))

    def interpretedRecording(self, new, transform, parents):
        template = ('[provenance] Recorded the command [{1}] to create [{0}] '+
            'based on [{2}]')
        print(template.format(new, transform, ', '.join(parents)))
    
