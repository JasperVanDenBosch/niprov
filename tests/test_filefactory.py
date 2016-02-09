import unittest
from mock import Mock, patch

class FileFactoryTests(unittest.TestCase):

    def setUp(self):
        self.log = Mock()
        self.libs = Mock()
        self.libs.hasDependency.return_value = True
        self.log = Mock()
        self.location = Mock()
        self.location.toDictionary.return_value = {'path':''}
        self.locationFactory = Mock()
        self.locationFactory.fromString.return_value = self.location
        self.dependencies = Mock()
        self.dependencies.getLocationFactory.return_value = self.locationFactory
        self.dependencies.getListener.return_value = self.log
        self.dependencies.getLibraries.return_value = self.libs

    def test_BaseFile(self):
        from niprov.files import FileFactory
        from niprov.basefile import BaseFile
        factory = FileFactory(dependencies=self.dependencies)
        fileCreated = factory.locatedAt('example.f')
        self.assertIsInstance(fileCreated, BaseFile)

    def test_If_parrec_passed_uses_ParrecFile(self):
        from niprov.files import FileFactory
        from niprov.parrec import ParrecFile
        factory = FileFactory(dependencies=self.dependencies)
        fileCreated = factory.locatedAt('example.PAR')
        self.assertIsInstance(fileCreated, ParrecFile)

    def test_If_nii_passed_uses_NiftiFile(self):
        from niprov.files import FileFactory
        from niprov.nifti import NiftiFile
        factory = FileFactory(dependencies=self.dependencies)
        fileCreated = factory.locatedAt('example.nii')
        self.assertIsInstance(fileCreated, NiftiFile)

    def test_If_compressed_nii_passed_uses_NiftiFile(self):
        from niprov.files import FileFactory
        from niprov.nifti import NiftiFile
        factory = FileFactory(dependencies=self.dependencies)
        fileCreated = factory.locatedAt('example.nii.gz')
        self.assertIsInstance(fileCreated, NiftiFile)

    def test_If_dicom_passed_uses_DicomFile(self):
        from niprov.files import FileFactory
        from niprov.dcm import DicomFile
        factory = FileFactory(dependencies=self.dependencies)
        fileCreated = factory.locatedAt('example.dcm')
        self.assertIsInstance(fileCreated, DicomFile)

    def test_If_fif_passed_uses_FifFile(self):
        from niprov.files import FileFactory
        from niprov.fif import FifFile
        factory = FileFactory(dependencies=self.dependencies)
        fileCreated = factory.locatedAt('example.fif')
        self.assertIsInstance(fileCreated, FifFile)

    def test_If_dcm_passed_but_pydicom_not_installed_tells_listener(self):
        from niprov.files import FileFactory
        from niprov.basefile import BaseFile
        self.libs.hasDependency.return_value = False
        factory = FileFactory(dependencies=self.dependencies)
        fileCreated = factory.locatedAt('example.dcm')
        self.assertIsInstance(fileCreated, BaseFile)
        self.log.missingDependencyForImage.assert_called_with('dicom','example.dcm')

    def test_If_parrec_passed_but_nibabel_not_installed_tells_listener(self):
        from niprov.files import FileFactory
        from niprov.basefile import BaseFile
        self.libs.hasDependency.return_value = False
        factory = FileFactory(dependencies=self.dependencies)
        fileCreated = factory.locatedAt('example.PAR')
        self.assertIsInstance(fileCreated, BaseFile)
        self.log.missingDependencyForImage.assert_called_with('nibabel','example.PAR')

    def test_If_fif_passed_but_mne_not_installed_tells_listener(self):
        from niprov.files import FileFactory
        from niprov.basefile import BaseFile
        self.libs.hasDependency.return_value = False
        factory = FileFactory(dependencies=self.dependencies)
        fileCreated = factory.locatedAt('example.fif')
        self.assertIsInstance(fileCreated, BaseFile)
        self.log.missingDependencyForImage.assert_called_with('mne','example.fif')

    def test_If_extensions_are_not_case_sensitive(self):
        from niprov.files import FileFactory
        from niprov.dcm import DicomFile
        factory = FileFactory(dependencies=self.dependencies)
        fileCreated = factory.locatedAt('example.dCm')
        self.assertIsInstance(fileCreated, DicomFile)

    def test_fromProvenance_inserts_existing_provenance(self):
        import niprov.files
        niprov.files.BaseFile = Mock()
        niprov.files.DicomFile = Mock()
        niprov.files.FileFactory.formats['.dcm'] = ('dicom', niprov.files.DicomFile)
        factory = niprov.files.FileFactory(dependencies=self.dependencies)
        inProvenance = {'location':'some.file','aproperty':'avalue'}
        inProvenanceDcm = {'location':'some.dcm','aproperty':'avalue'}
        fileCreated = factory.fromProvenance(inProvenance)
        niprov.files.BaseFile.assert_called_with('some.file', 
            provenance=inProvenance, dependencies=self.dependencies)
        fileCreated = factory.fromProvenance(inProvenanceDcm)
        niprov.files.DicomFile.assert_called_with('some.dcm', 
            provenance=inProvenanceDcm, dependencies=self.dependencies)

    def test_If_cnt_passed_uses_NeuroscanFile(self):
        from niprov.files import FileFactory
        from niprov.cnt import NeuroscanFile
        factory = FileFactory(dependencies=self.dependencies)
        fileCreated = factory.locatedAt('example.cnt')
        self.assertIsInstance(fileCreated, NeuroscanFile)

    def test_fromProvenance_inserts_provenance_also_if_lib_missing(self):
        import niprov.files
        self.libs.hasDependency.return_value = False
        with patch('niprov.files.BaseFile') as BaseFileCtor:
            factory = niprov.files.FileFactory(dependencies=self.dependencies)
            inProvenance = {'location':'some.dcm','aproperty':'avalue'}
            fileCreated = factory.fromProvenance(inProvenance)
            BaseFileCtor.assert_called_with('some.dcm', 
                provenance=inProvenance, dependencies=self.dependencies)





