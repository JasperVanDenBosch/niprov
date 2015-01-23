import unittest
from mock import Mock
from datetime import datetime

class InspectionTests(unittest.TestCase):

    def test_Loads_file_with_nibabel(self):
        import niprov.inspection
        log = Mock()
        libs = self.setupNibabel()
        libs.hasDependency.return_value = True
        filesys = Mock()
        niprov.inspection.inspect('/p/f1.PAR', listener=log, libs=libs, filesystem=filesys)
        libs.nibabel.load.assert_any_call('/p/f1.PAR')

    def test_Doesnt_use_nibabel_if_not_installed(self):
        import niprov.inspection
        log = Mock()
        libs = self.setupNibabel()
        libs.hasDependency.return_value = False
        filesys = Mock()
        provenance = niprov.inspection.inspect('/p/f1.PAR', listener=log, libs=libs, filesystem=filesys)
        self.assertRaises(AssertionError,
            libs.nibabel.load.assert_any_call, '/p/f1.PAR')

    def test_If_dcm_passed_uses_pydicom_to_open(self):
        import niprov.inspection
        log = Mock()
        libs = self.setupPydicom()
        libs.hasDependency.return_value = True
        filesys = Mock()
        provenance = niprov.inspection.inspect('/p/f1.dcm', listener=log, libs=libs, filesystem=filesys)
        # doesnt complain about missing pydicom        
        self.assertRaises(AssertionError,
            log.missingDependencyForImage.assert_any_call, 'dicom','/p/f1.dcm')
        # uses pydicom
        libs.dicom.read_file.assert_any_call('/p/f1.dcm')

    def test_If_dcm_passed_but_pydicom_not_installed_tells_listener(self):
        import niprov.inspection
        log = Mock()
        libs = self.setupPydicom()
        libs.hasDependency.return_value = False
        filesys = Mock()
        provenance = niprov.inspection.inspect('/p/f1.dcm', listener=log, libs=libs, filesystem=filesys)
        self.assertRaises(AssertionError,
            libs.dicom.read_file.assert_any_call, '/p/f1.dcm')
        log.missingDependencyForImage.assert_any_call('dicom','/p/f1.dcm')

    def test_If_nothing_inspected_returns_None(self):
        import niprov.inspection
        log = Mock()
        libs = self.setupNibabel()
        libs.hasDependency.return_value = False
        filesys = Mock()
        provenance = niprov.inspection.inspect('/p/f1.PAR', listener=log, libs=libs, filesystem=filesys)
        self.assertIsNone(provenance)

    def test_Gets_basic_info_from_nibabel_and_returns_it(self):
        import niprov.inspection
        log = Mock()
        libs = self.setupNibabel()
        libs.hasDependency.return_value = True
        filesys = Mock()
        out = niprov.inspection.inspect('/p/f1.PAR', listener=log, libs=libs, filesystem=filesys)
        self.assertEqual(out['subject'], 'John Doeish')
        self.assertEqual(out['protocol'], 'T1 SENSE')
        self.assertEqual(out['acquired'], datetime(2014, 8, 5, 11, 27, 34))

    def test_Gets_basic_info_from_pydicom_and_returns_it(self):
        import niprov.inspection
        log = Mock()
        libs = self.setupPydicom()
        libs.hasDependency.return_value = True
        filesys = Mock()
        out = niprov.inspection.inspect('/p/f1.dcm', listener=log, libs=libs, filesystem=filesys)
        self.assertEqual(out['subject'], 'John Doeish')
        self.assertEqual(out['protocol'], 'T1 SENSE')
        self.assertEqual(out['acquired'], datetime(2014, 8, 5, 12, 19, 14))

    def test_Saves_file_path_along_with_provenance(self):
        import niprov.inspection
        log = Mock()
        libs = self.setupPydicom()
        libs.hasDependency.return_value = True
        filesys = Mock()
        out = niprov.inspection.inspect('/p/f1.dcm', listener=log, libs=libs, filesystem=filesys)
        self.assertEqual(out['path'], '/p/f1.dcm')

    def test_Saves_filesize_along_with_provenance(self):
        import niprov.inspection
        log = Mock()
        libs = self.setupPydicom()
        libs.hasDependency.return_value = True
        filesys = Mock()
        out = niprov.inspection.inspect('/p/f1.dcm', listener=log, libs=libs, filesystem=filesys)
        self.assertEqual(out['size'], filesys.getsize('/p/f1.dcm'))

    def test_If_error_during_inspection_tells_listener_and_returns_None(self):
        import niprov.inspection
        log = Mock()
        libs = Mock()
        libs.hasDependency.return_value = True
        libs.nibabel.load.side_effect = ValueError
        filesys = Mock()
        out = niprov.inspection.inspect('/p/f1.PAR', listener=log, libs=libs, filesystem=filesys)
        self.assertIsNone(out)
        log.fileError.assert_any_call('/p/f1.PAR')


    def setupNibabel(self):
        libs = Mock()
        img = Mock()
        img.header.general_info = {
            'exam_date':'2014.08.05 / 11:27:34',
            'protocol_name':'T1 SENSE',
            'patient_name':'John Doeish'}
        libs.nibabel.load.return_value = img
        return libs

    def setupPydicom(self):
        libs = Mock()
        img = Mock()
        img.AcquisitionDateTime = '20140805121914.59000'
        img.SeriesDescription = 'T1 SENSE'
        img.PatientID = 'John Doeish'
        libs.dicom.read_file.return_value = img
        return libs        

