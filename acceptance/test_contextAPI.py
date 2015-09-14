import unittest
import os, shutil


class ContextApiTests(unittest.TestCase):

    def setUp(self):
        self.dbpath = os.path.expanduser(os.path.join('~','provenance.json'))
        if os.path.exists(self.dbpath):
            shutil.move(self.dbpath, self.dbpath.replace('.json','.backup.json'))
        os.mkdir('temp')

    def tearDown(self):
        if os.path.exists(self.dbpath):
            shutil.move(self.dbpath, self.dbpath.replace('.json','.test.json'))
        shutil.rmtree('temp')

    def touch(self, path):
        with open(path,'w') as tempfile:
            tempfile.write('0')

    def test_Log(self):
        from niprov import Context
        provenance = Context()
        provenance.discover('testdata')
        newfile = 'temp/smoothed.test'
        self.touch(newfile)
        provenance.log(newfile, 'test', 'testdata/eeg/stub.cnt')
        img = provenance.report(forFile=newfile)
        self.assertEqual(img.provenance['subject'], 'Jane Doe')
        self.assertEqual(img.provenance['size'], os.path.getsize(newfile))

