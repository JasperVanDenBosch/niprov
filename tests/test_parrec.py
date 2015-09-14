import unittest
from mock import Mock
from datetime import datetime
from tests.test_basefile import BaseFileTests


class ParrecTests(BaseFileTests):

    def setUp(self):
        super(ParrecTests, self).setUp()
        self.libs = Mock()
        self.dependencies.getLibraries.return_value = self.libs
        self.setupNibabel()
        from niprov.parrec import ParrecFile
        self.constructor = ParrecFile
        self.file = ParrecFile(self.path, dependencies=self.dependencies)

    def test_Gets_basic_info_from_nibabel_and_returns_it(self):
        out = self.file.inspect()
        self.assertEqual(out['subject'], 'John Doeish')
        self.assertEqual(out['protocol'], 'T1 SENSE')
        self.assertEqual(out['acquired'], datetime(2014, 8, 5, 11, 27, 34))

    def test_Gets_dimensions(self):
        out = self.file.inspect()
        self.assertEqual(out['dimensions'], [80,80,10])

    def setupNibabel(self):
        img = Mock()
        img.header.general_info = {
            'exam_date':'2014.08.05 / 11:27:34',
            'protocol_name':'T1 SENSE',
            'patient_name':'John Doeish'}
        img.shape = (80,80,10)
        self.libs.nibabel.load.return_value = img
        self.libs.hasDependency.return_value = True

