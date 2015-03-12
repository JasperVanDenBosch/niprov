import unittest
import os, shutil


class ApiTests(unittest.TestCase):

    def setUp(self):
        self.dbpath = os.path.expanduser(os.path.join('~','provenance.json'))
        if os.path.exists(self.dbpath):
            shutil.move(self.dbpath, self.dbpath.replace('.json','.backup.json'))

    def tearDown(self):
        if os.path.exists(self.dbpath):
            shutil.move(self.dbpath, self.dbpath.replace('.json','.test.json'))

    def test_Discover(self):
        import niprov
        niprov.discover('testdata')
        provenance = niprov.report(forFile='testdata/dicom/T1.dcm')
        self.assertEqual(provenance['dimensions'], [80, 80, 10])
        provenance = niprov.report(forFile='testdata/eeg/stub.cnt')
        self.assertEqual(provenance['subject'], 'Jane Doe')

    def test_Rename(self):
        try:
            import niprov
            files, directory = self.createExtensionlessFiles()
            niprov.renameDicoms(directory)
            assert not os.path.isfile(files[0])
            assert os.path.isfile(files[0]+'.dcm')
        finally:
            self.clearDicomfiles()

    def createExtensionlessFiles(self):
        if not os.path.exists('dicomdir'):
            os.makedirs('dicomdir')
        files = []
        for n in range(5):
            f = os.path.join('dicomdir',str(n))
            files.append(f)
            with open(f,'w') as fhandle:
                fhandle.write('x')
        return files, 'dicomdir'

    def clearDicomfiles(self):
        shutil.rmtree('dicomdir')


