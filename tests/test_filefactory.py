import unittest
from mock import Mock

class FileFactoryTests(unittest.TestCase):

    def setUp(self):
        self.log = Mock()
        self.libs = Mock()
        self.libs.hasDependency.return_value = True
        self.log = Mock()

    def test_BaseFile(self):
        from niprov.files import FileFactory
        from niprov.basefile import BaseFile
        factory = FileFactory(libs=self.libs, listener=self.log)
        fileCreated = factory.locatedAt('example.f')
        self.assertIsInstance(fileCreated, BaseFile)

    def test_If_parrec_passed_uses_ParrecFile(self):
        from niprov.files import FileFactory
        from niprov.parrec import ParrecFile
        factory = FileFactory(libs=self.libs, listener=self.log)
        fileCreated = factory.locatedAt('example.PAR')
        self.assertIsInstance(fileCreated, ParrecFile)

    def test_If_dicom_passed_uses_DicomFile(self):
        from niprov.files import FileFactory
        from niprov.dcm import DicomFile
        factory = FileFactory(libs=self.libs, listener=self.log)
        fileCreated = factory.locatedAt('example.dcm')
        self.assertIsInstance(fileCreated, DicomFile)

    def test_If_fif_passed_uses_FifFile(self):
        from niprov.files import FileFactory
        from niprov.fif import FifFile
        factory = FileFactory(libs=self.libs, listener=self.log)
        fileCreated = factory.locatedAt('example.fif')
        self.assertIsInstance(fileCreated, FifFile)

    def test_If_dcm_passed_but_pydicom_not_installed_tells_listener(self):
        from niprov.files import FileFactory
        from niprov.basefile import BaseFile
        self.libs.hasDependency.return_value = False
        factory = FileFactory(libs=self.libs, listener=self.log)
        fileCreated = factory.locatedAt('example.dcm')
        self.assertIsInstance(fileCreated, BaseFile)
        self.log.missingDependencyForImage.assert_called_with('dicom','example.dcm')

    def test_If_parrec_passed_but_nibabel_not_installed_tells_listener(self):
        from niprov.files import FileFactory
        from niprov.basefile import BaseFile
        self.libs.hasDependency.return_value = False
        factory = FileFactory(libs=self.libs, listener=self.log)
        fileCreated = factory.locatedAt('example.PAR')
        self.assertIsInstance(fileCreated, BaseFile)
        self.log.missingDependencyForImage.assert_called_with('nibabel','example.PAR')

    def test_If_fif_passed_but_mne_not_installed_tells_listener(self):
        from niprov.files import FileFactory
        from niprov.basefile import BaseFile
        self.libs.hasDependency.return_value = False
        factory = FileFactory(libs=self.libs, listener=self.log)
        fileCreated = factory.locatedAt('example.fif')
        self.assertIsInstance(fileCreated, BaseFile)
        self.log.missingDependencyForImage.assert_called_with('mne','example.fif')

    def test_If_extensions_are_not_case_sensitive(self):
        from niprov.files import FileFactory
        from niprov.dcm import DicomFile
        factory = FileFactory(libs=self.libs, listener=self.log)
        fileCreated = factory.locatedAt('example.dCm')
        self.assertIsInstance(fileCreated, DicomFile)

    def test_fromProvenance_inserts_existing_provenance(self):
        import niprov.files
        niprov.files.BaseFile = Mock()
        niprov.files.DicomFile = Mock()
        niprov.files.FileFactory.formats['.dcm'] = ('dicom', niprov.files.DicomFile)
        factory = niprov.files.FileFactory(libs=self.libs, listener=self.log)
        inProvenance = {'path':'some.file','aproperty':'avalue'}
        inProvenanceDcm = {'path':'some.dcm','aproperty':'avalue'}
        fileCreated = factory.fromProvenance(inProvenance)
        niprov.files.BaseFile.assert_called_with('some.file', provenance=inProvenance)
        fileCreated = factory.fromProvenance(inProvenanceDcm)
        niprov.files.DicomFile.assert_called_with('some.dcm', provenance=inProvenanceDcm)

    def test_If_cnt_passed_uses_NeuroscanFile(self):
        from niprov.files import FileFactory
        from niprov.cnt import NeuroscanFile
        factory = FileFactory(libs=self.libs, listener=self.log)
        fileCreated = factory.locatedAt('example.cnt')
        self.assertIsInstance(fileCreated, NeuroscanFile)




