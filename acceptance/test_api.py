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

