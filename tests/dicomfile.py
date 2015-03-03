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

    def test_if_doesnt_have_acqDateTime_get_seriesDatetime(self):
        del(self.img.AcquisitionDateTime)
        self.img.SeriesDate = '20120416'
        self.img.SeriesTime = '101330.60000'
        out = self.file.inspect()
        self.assertEqual(out['acquired'], 
            datetime(2012, 4, 16, 20, 8, 50, 600000))

    def setupPydicom(self):
        self.img = Mock()
        self.img.AcquisitionDateTime = '20140805121914.59000'
        self.img.SeriesDescription = 'T1 SENSE'
        self.img.PatientID = 'John Doeish'
        self.libs.dicom.read_file.return_value = self.img
        self.libs.hasDependency.return_value = True

