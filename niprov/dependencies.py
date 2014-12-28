#!/usr/bin/python
# -*- coding: UTF-8 -*-


class Dependencies(object):

    def __init__(self):
        try:
            import nibabel
            self.nibabel = nibabel
        except:
            self.nibabel = None
        try:
            import dicom
            self.dicom = dicom
        except:
            self.dicom = None


    def hasDependency(self, libname):
        return getattr(self, libname)

    
