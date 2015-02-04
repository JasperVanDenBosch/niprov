import unittest
from mock import Mock
from datetime import datetime
from tests.basefile import BasicInspectionTests


class ParrecTests(BasicInspectionTests):

    def setUp(self):
        super(ParrecTests, self).setUp()
        self.libs = Mock()
        self.setupNibabel()
        from niprov.parrec import ParrecFile
        self.file = ParrecFile(self.path, listener=self.log, 
            filesystem=self.filesys, hasher=self.hasher, dependencies=self.libs,
            serializer=self.json)

    def test_If_error_during_inspection_tells_listener_and_returns_None(self):
        self.libs.nibabel.load.side_effect = ValueError
        out = self.file.inspect()
        self.log.fileError.assert_called_with(self.path)

    def test_Gets_basic_info_from_nibabel_and_returns_it(self):
        out = self.file.inspect()
        self.assertEqual(out['subject'], 'John Doeish')
        self.assertEqual(out['protocol'], 'T1 SENSE')
        self.assertEqual(out['acquired'], datetime(2014, 8, 5, 11, 27, 34))

    def setupNibabel(self):
        img = Mock()
        img.header.general_info = {
            'exam_date':'2014.08.05 / 11:27:34',
            'protocol_name':'T1 SENSE',
            'patient_name':'John Doeish'}
        self.libs.nibabel.load.return_value = img
        self.libs.hasDependency.return_value = True

