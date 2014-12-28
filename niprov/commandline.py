#!/usr/bin/python
# -*- coding: UTF-8 -*-


class Commandline(object):

    def fileFound(self, fname, provenance):
        template = '{1[acquired]} {1[subject]} {1[protocol]:24} {0}'
        print(template.format(fname,provenance))

    def missingDependencyForImage(self, lib, fpath):
        template = 'Missing python package "{0}" to read file: {1}'        
        print(template.format(lib, fpath))

    def fileError(self, fpath):
        print('Error opening file: {0}'.format(fpath))
    
