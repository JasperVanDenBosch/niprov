import unittest
import os, shutil


class ContextApiTests(unittest.TestCase):

    def setUp(self):
        self.dbpath = os.path.expanduser(os.path.join('~','provenance_test.json'))
        if os.path.exists(self.dbpath):
            os.remove(self.dbpath)
        os.mkdir('temp')
        from niprov import Context
        self.provenance = Context()
        self.provenance.config.database_type = 'file'
        self.provenance.config.database_url = self.dbpath

    def tearDown(self):
        shutil.rmtree('temp')

    def touch(self, path):
        with open(path,'w') as tempfile:
            tempfile.write('0')

    def test_Log(self):
        self.provenance.discover('testdata')
        newfile = 'temp/smoothed.test'
        self.touch(newfile)
        parent = os.path.abspath('testdata/eeg/stub.cnt')
        self.provenance.log(newfile, 'test', parent)
        testfpath = os.path.abspath(newfile)
        img = self.provenance.report(forFile=testfpath)
        self.assertEqual(img.provenance['subject'], 'Jane Doe')
        self.assertEqual(img.provenance['size'], os.path.getsize(newfile))

    def test_Export_Import(self):
        from niprov.exceptions import UnknownFileError
        self.provenance.discover('testdata')
        discoveredFile = os.path.abspath('testdata/eeg/stub.cnt')
        self.assertIsNotNone(self.provenance.report(forFile=discoveredFile))
        backupFilepath = self.provenance.export()
        os.remove(self.dbpath) # get rid of existing data.
        with self.assertRaises(UnknownFileError):
            self.provenance.report(forFile=discoveredFile)
        self.provenance.importp(backupFilepath)
        self.assertIsNotNone(self.provenance.report(forFile=discoveredFile))

    def test_Attach_provenance_string_in_file_based_on_config(self):
        import nibabel
        self.provenance.config.attach = True
        newfile = 'temp/fileX.nii.gz'
        shutil.copy('testdata/nifti/fieldmap.nii.gz', newfile)
        self.provenance.add(newfile)
        img = nibabel.load(newfile)
        self.assertEqual(img.get_header().extensions.count('comment'), 1)
        self.assertEqual(img.get_header().extensions[0].get_code(), 'comment')
        content = img.get_header().extensions[0].get_content()
        self.assertIn('"location": "{0}"'.format(newfile), content)
        
        

if __name__ == '__main__':
    unittest.main()

