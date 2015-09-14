import unittest
from mock import Mock
from datetime import datetime
from tests.test_basefile import BaseFileTests


class NiftiTests(BaseFileTests):

    def setUp(self):
        super(NiftiTests, self).setUp()
        self.libs = Mock()
        self.dependencies.getLibraries.return_value = self.libs
        self.img = Mock()
        self.hdr = Mock()
        self.setupNibabel()
        from niprov.nifti import NiftiFile
        self.constructor = NiftiFile
        self.file = NiftiFile(self.path, dependencies=self.dependencies)

    def setupNibabel(self):
        # Extension constructor simply creates a tuple of arguments
        self.img.get_header.return_value = self.hdr
        self.libs.nibabel.nifti1.Nifti1Extension = lambda x,y: ('extension',x,y)
        self.libs.nibabel.load.return_value = self.img
        self.libs.hasDependency.return_value = True

    def test_Attach_method(self):
        self.file.provenance = {'foo':'bar'}
        self.file.attach()
        self.hdr.extensions.append.assert_called_with(('extension','comment', 
            self.json.serialize(self.file.provenance)))
        self.img.to_filename.assert_called_with(self.file.path)

