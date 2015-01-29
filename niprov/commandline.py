#!/usr/bin/python
# -*- coding: UTF-8 -*-


class Commandline(object):

    def fileFound(self, fname, provenance):
        template = '{0[path]}'
        print(template.format(provenance))

    def missingDependencyForImage(self, lib, fpath):
        template = 'Missing python package "{0}" to read file: {1}'        
        print(template.format(lib, fpath))

    def fileError(self, fpath):
        print('Error opening file: {0}'.format(fpath))
    
