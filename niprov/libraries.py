#!/usr/bin/python
# -*- coding: UTF-8 -*-


class Libraries(object):

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
        try:
            import mne.io
            self.mne = mne
        except:
            self.mne = None
        try:
            import mnefun
            self.mnefun = mnefun
        except:
            self.mnefun = None


    def hasDependency(self, libname):
        if libname is None:
            return True # don't need dependency
        return getattr(self, libname)

    
