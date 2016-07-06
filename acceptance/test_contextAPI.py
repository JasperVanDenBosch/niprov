import unittest
import os, shutil
from os.path import abspath


class ProvenanceContextApiTests(unittest.TestCase):

    def setUp(self):
        self.dbpath = os.path.expanduser(os.path.join('~','provenance_test.json'))
        if os.path.exists(self.dbpath):
            os.remove(self.dbpath)
        os.mkdir('temp')
        from niprov import ProvenanceContext
        self.provenance = ProvenanceContext()
        self.provenance.config.database_type = 'file'
        self.provenance.config.database_url = self.dbpath

    def tearDown(self):
        shutil.rmtree('temp')

    def touch(self, path):
        with open(path,'w') as tempfile:
            tempfile.write('0')

    def test_Relative_paths(self):
        self.provenance.discover('testdata')
        newfile = 'temp/smoothed.test'
        self.touch(newfile)
        self.provenance.log(newfile, 'test', 'testdata/eeg/stub.cnt')
        img = self.provenance.get().byLocation(newfile)

    def test_Log(self):
        self.provenance.discover('testdata')
        newfile = 'temp/smoothed.test'
        self.touch(newfile)
        parent = os.path.abspath('testdata/eeg/stub.cnt')
        self.provenance.log(newfile, 'test', parent)
        testfpath = os.path.abspath(newfile)
        img = self.provenance.get().byLocation(testfpath)
        self.assertEqual(img.provenance['subject'], 'Jane Doe')
        self.assertEqual(img.provenance['size'], os.path.getsize(newfile))

    def test_Record_with_user(self):
        self.provenance.discover('testdata')
        newfile = 'temp/recorded.test'
        self.touch(newfile)
        parent = os.path.abspath('testdata/eeg/stub.cnt')
        self.provenance.record('echo hallo', newfile, parent, user='007')
        testfpath = os.path.abspath(newfile)
        img = self.provenance.get().byLocation(testfpath)
        self.assertEqual(img.provenance['user'], '007')

    def test_Export_Import(self):
        from niprov.exceptions import UnknownFileError
        self.provenance.discover('testdata')
        discoveredFile = os.path.abspath('testdata/eeg/stub.cnt')
        self.assertIsNotNone(self.provenance.get().byLocation(discoveredFile))
        backupFilepath = self.provenance.backup()
        os.remove(self.dbpath) # get rid of existing data.
        self.assertIsNone(self.provenance.get().byLocation(discoveredFile))
        self.provenance.importp(backupFilepath)
        self.assertIsNotNone(self.provenance.get().byLocation(discoveredFile))

    @unittest.skip("Doesn't work on Travis right now.")
    def test_Attach_provenance_string_in_file_based_on_config(self):
        import nibabel
        self.provenance.config.attach = True
        newfile = os.path.abspath('temp/fileX.nii.gz')
        shutil.copy('testdata/nifti/fieldmap.nii.gz', newfile)
        self.provenance.add(newfile)
        img = nibabel.load(newfile)
        self.assertEqual(img.get_header().extensions.count('comment'), 1)
        self.assertEqual(img.get_header().extensions[0].get_code(), 6)
        content = img.get_header().extensions[0].get_content()
        self.assertIn('"path": "{0}"'.format(newfile), content)

    def test_Approval(self):
        self.provenance.discover('testdata')
        self.provenance.markForApproval(['testdata/parrec/T1.PAR',
                                'testdata/parrec/T2.PAR'])
        imgs = self.provenance.markedForApproval()
        self.provenance.approve('testdata/parrec/T1.PAR')
        imgs = self.provenance.markedForApproval()

    def test_Comparison(self):
        # Given two PARREC images' provenance records
        par1 = self.provenance.add(abspath('testdata/parrec/T1.PAR'))
        par2 = self.provenance.add(abspath('testdata/parrec/T2.PAR'))
        # Comparing them returns a Diff object with methods testing equality
        self.assertFalse(self.provenance.compare(par1, par2).areEqual())
        # Compare() can also be called as a method on the objects themselves,
        # and the Diff object has assert..() methods that raise AssertionErrors
        msgRegExp = ".*echo-time.*2\.08.*80\.0.*"
        with self.assertRaisesRegexp(AssertionError, msgRegExp):
            par1.compare(par2).assertEqualProtocol()

    def test_Search(self):
        x1 = self.provenance.add('x1', transient=True,
            provenance={'transformation':'needle and thread'})
        x2 = self.provenance.add('x2/needle.y', transient=True, 
            provenance={'transformation':'needle and thread'})
        x3 = self.provenance.add('x3', transient=True, 
            provenance={'transformation':'hammer and tongs'})
        results = self.provenance.search('needle')
        self.assertEqual(len(results), 2)
        self.assertEqual(x2.provenance['id'], results[0].provenance['id'])
        self.assertEqual(x1.provenance['id'], results[1].provenance['id'])

    def test_GetModalities(self):
        self.provenance.discover('testdata')
        modalities = self.provenance.get().allModalities()
        self.assertIn('MRI', modalities)
        self.assertIn('DWI', modalities)
        self.assertIn('EEG', modalities)

    def test_Version_history(self):
        self.provenance.add('f', transient=True, provenance={'a':1})
        img = self.provenance.get().byLocation('f')
        self.assertEqual(1, img.provenance['a'])
        self.provenance.add('f', transient=True, provenance={'a':2})
        img = self.provenance.get().byLocation('f')
        self.assertEqual(2, img.provenance['a'])
        self.assertEqual(1, img.versions[-1]['a'])
        self.provenance.add('f', transient=True, provenance={'a':3})
        img = self.provenance.get().byLocation('f')
        self.assertEqual(3, img.provenance['a'])
        self.assertEqual(2, img.versions[-1]['a'])
        self.assertEqual(1, img.versions[-2]['a'])

    def test_If_no_parent_provided_found_copy_considered_parent(self):
        self.provenance.add('testdata/eeg/stub.cnt')
        self.touch('temp/orig.f')
        self.provenance.log('temp/orig.f', 'op1', 'testdata/eeg/stub.cnt')
        shutil.copy('temp/orig.f', 'temp/copy.f')
        self.touch('temp/child.f')
        child = self.provenance.log('temp/child.f', 'op2', 'temp/copy.f')
        self.assertEqual(child.provenance['subject'], 'Jane Doe')
        copy = self.provenance.get().byLocation('temp/copy.f')
        self.assertIn('temp/orig.f', copy.provenance['parents'][0])
 

if __name__ == '__main__':
    unittest.main()

