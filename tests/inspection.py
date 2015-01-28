import unittest
from mock import Mock
from datetime import datetime

class InspectionTests(unittest.TestCase):

    def setUp(self):
        self.log = Mock()
        self.libs = self.setupNibabel()
        self.libs.hasDependency.return_value = True
        self.hasher = Mock()
        self.filesys = Mock()
        self.hasher = Mock()

    def callInspect(self, fname):
        import niprov.inspection
        return niprov.inspection.inspect(fname, 
            listener=self.log, 
            libs=self.libs, 
            filesystem=self.filesys,
            hasher=self.hasher)

    def test_If_nothing_inspected_returns_None(self):
        self.libs.hasDependency.return_value = False
        provenance = self.callInspect('/p/f1.PAR')
        self.assertIsNone(provenance)

    def test_Gets_basic_info_from_nibabel_and_returns_it(self):
        out = self.callInspect('/p/f1.PAR')
        self.assertEqual(out['subject'], 'John Doeish')
        self.assertEqual(out['protocol'], 'T1 SENSE')
        self.assertEqual(out['acquired'], datetime(2014, 8, 5, 11, 27, 34))

    def test_Gets_basic_info_from_pydicom_and_returns_it(self):
        self.libs = self.setupPydicom()
        out = self.callInspect('/p/f1.dcm')
        self.assertEqual(out['subject'], 'John Doeish')
        self.assertEqual(out['protocol'], 'T1 SENSE')
        self.assertEqual(out['acquired'], datetime(2014, 8, 5, 12, 19, 14))

    def test_Saves_file_path_along_with_provenance(self):
        self.libs = self.setupPydicom()
        out = self.callInspect('/p/f1.dcm')
        self.assertEqual(out['path'], '/p/f1.dcm')

    def test_Saves_filesize_along_with_provenance(self):
        self.libs = self.setupPydicom()
        out = self.callInspect('/p/f1.dcm')
        self.assertEqual(out['size'], self.filesys.getsize('/p/f1.dcm'))

    def test_Saves_file_creation_time_along_with_provenance(self):
        self.libs = self.setupPydicom()
        out = self.callInspect('/p/f1.dcm')
        self.assertEqual(out['created'], self.filesys.getctime('/p/f1.dcm'))

    def test_If_error_during_inspection_tells_listener_and_returns_None(self):
        self.libs.nibabel.load.side_effect = ValueError
        out = self.callInspect('/p/f1.PAR')
        self.assertIsNone(out)
        self.log.fileError.assert_any_call('/p/f1.PAR')

    def test_Asks_hasher_for_digest_of_file(self):
        out = self.callInspect('/p/f1.PAR')
        self.assertEqual(out['hash'], self.hasher.digest('/p/f1.PAR'))


    def setupNibabel(self):
        libs = Mock()
        img = Mock()
        img.header.general_info = {
            'exam_date':'2014.08.05 / 11:27:34',
            'protocol_name':'T1 SENSE',
            'patient_name':'John Doeish'}
        libs.nibabel.load.return_value = img
        libs.hasDependency.return_value = True
        return libs

    def setupPydicom(self):
        libs = Mock()
        img = Mock()
        img.AcquisitionDateTime = '20140805121914.59000'
        img.SeriesDescription = 'T1 SENSE'
        img.PatientID = 'John Doeish'
        libs.dicom.read_file.return_value = img
        libs.hasDependency.return_value = True
        return libs        

