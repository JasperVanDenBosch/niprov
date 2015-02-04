import unittest
from mock import Mock
from datetime import datetime
from tests.basefile import BasicInspectionTests


class DicomTests(BasicInspectionTests):

    def setUp(self):
        super(DicomTests, self).setUp()
        self.libs = Mock()
        self.setupPydicom()
        from niprov.dcm import DicomFile
        self.file = DicomFile(self.path, listener=self.log, 
            filesystem=self.filesys, hasher=self.hasher, dependencies=self.libs,
            serializer=self.json)

    def test_Gets_basic_info_from_pydicom_and_returns_it(self):
        out = self.file.inspect()
        self.assertEqual(out['subject'], 'John Doeish')
        self.assertEqual(out['protocol'], 'T1 SENSE')
        self.assertEqual(out['acquired'], datetime(2014, 8, 5, 12, 19, 14))

    def test_If_error_during_inspection_tells_listener_and_returns_None(self):
        self.libs.dicom.read_file.side_effect = ValueError
        out = self.file.inspect()
        self.log.fileError.assert_called_with(self.path)

    def setupPydicom(self):
        img = Mock()
        img.AcquisitionDateTime = '20140805121914.59000'
        img.SeriesDescription = 'T1 SENSE'
        img.PatientID = 'John Doeish'
        self.libs.dicom.read_file.return_value = img
        self.libs.hasDependency.return_value = True

