import unittest
from mock import Mock
from datetime import datetime
from tests.basefile import BasicInspectionTests


class NiftiTests(BasicInspectionTests):

    def setUp(self):
        super(NiftiTests, self).setUp()
        self.libs = Mock()
#        from niprov.nifti import NiftiFile
#        self.file = NiftiFile(self.path, listener=self.log, 
#            filesystem=self.filesys, hasher=self.hasher, dependencies=self.libs,
#            serializer=self.json)


#  dump_ext = nifti1.Nifti1Extension('comment', 'content')
#  nhdr.extensions.append(dump_ext)

