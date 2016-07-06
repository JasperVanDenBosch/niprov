import unittest
from mock import Mock, MagicMock, PropertyMock
from datetime import datetime
from tests.test_basefile import BaseFileTests


class DicomTests(BaseFileTests):

    def setUp(self):
        super(DicomTests, self).setUp()
        self.libs = Mock()
        self.dependencies.getLibraries.return_value = self.libs
        self.setupPydicom()
        from niprov.dcm import DicomFile
        self.constructor = DicomFile
        self.file = DicomFile(self.path, dependencies=self.dependencies)

    def test_Gets_basic_info_from_pydicom_and_returns_it(self):
        out = self.file.inspect()
        self.assertEqual(out['subject'], 'John Doeish')
        self.assertEqual(out['protocol'], 'T1 SENSE')
        self.assertEqual(out['acquired'], datetime(2014, 8, 5, 12, 19, 14))

    def test_if_doesnt_have_acqDateTime_get_seriesDatetime(self):
        del(self.img.AcquisitionDateTime)
        self.img.SeriesDate = '20120416'
        self.img.SeriesTime = '101330.60000'
        h = datetime.fromtimestamp(101330.60000).hour
        out = self.file.inspect()
        self.assertEqual(out['acquired'], 
            datetime(2012, 4, 16, h, 8, 50))

    def test_Series_interface(self):
        self.assertEqual(self.file.getSeriesId(), self.img.SeriesInstanceUID)
        self.assertIn(self.file.path, self.file.provenance['filesInSeries'])
        newFile = Mock()
        otherFile = Mock()
        out = self.file.mergeWith(newFile)
        self.assertIn(newFile.path, self.file.provenance['filesInSeries'])
        self.assertEqual(self.file, out)
        self.assertEqual('series-new-file', self.file.status)
        self.assertTrue(self.file.hasFile(newFile))
        self.assertFalse(self.file.hasFile(otherFile))

    def test_Gets_dimensions(self):
        out = self.file.inspect()
        self.assertEqual(out['dimensions'], [11, 12, 13])
        del(self.img.NumberOfFrames)
        out = self.file.inspect()
        self.assertEqual(out['dimensions'], [11, 12, 1])
        self.file.mergeWith(Mock())
        self.assertEqual(out['dimensions'], [11, 12, 2])

    def test_Gets_other_fields(self):
        out = self.file.inspect()
        self.assertEqual(out['duration'], 65.04713439941406)
        self.assertEqual(out['subject-position'], 'HFS')
        self.assertEqual(out['water-fat-shift'], 1.1173381805419922)

    def test_File_without_Rows(self):
        del(self.img.Rows)
        out = self.file.inspect()
        assert not self.listener.fileError.called
        self.assertNotIn('dimensions', out)
        del(self.img.NumberOfFrames)
        out = self.file.inspect()
        self.file.mergeWith(Mock())
        assert not self.listener.fileError.called

    def test_Determines_modality(self):
        out = self.file.inspect()
        self.assertEqual(out['modality'], 'MRI')

    def test_Preserves_modality_if_inherited(self):
        pass # Doesn't have to preserve

    def setupPydicom(self):
        self.img = Mock()
        self.img.AcquisitionDateTime = '20140805121914.59000'
        self.img.AcquisitionDuration = 65.04713439941406
        self.img.SeriesDescription = 'T1 SENSE'
        self.img.PatientID = 'John Doeish'
        self.img.PatientPosition = 'HFS'
        self.img.SeriesInstanceUID = '1.3.46.670589.11.17388.5.0.6340.2011121308140690488'
        self.img.Rows = 11
        self.img.Columns = 12
        self.img.NumberOfFrames = 13
        wfs = Mock()
        wfs.value = 1.1173381805419922
        self.img.__getitem__ = Mock(side_effect=lambda x: {(0x2001, 0x1022):wfs}[x])
        self.libs.dicom.read_file.return_value = self.img
        self.libs.hasDependency.return_value = True

