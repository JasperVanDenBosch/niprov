import unittest
from mock import Mock
from datetime import datetime
from tests.basefile import BaseFileTests


class FifTests(BaseFileTests):

    def setUp(self):
        super(FifTests, self).setUp()
        self.libs = Mock()
        self.setupMne()
        from niprov.fif import FifFile
        self.constructor = FifFile
        self.file = FifFile(self.path, listener=self.log, 
            filesystem=self.filesys, hasher=self.hasher, dependencies=self.libs,
            serializer=self.json)

    def test_Gets_basic_info_from_mne_and_returns_it(self):
        out = self.file.inspect()
        self.assertEqual(out['subject'], 'John Doeish')
        self.assertEqual(out['project'], 'worlddom')
        self.assertEqual(out['acquired'], self.acquired)

    def test_Gets_dimensions(self):
        out = self.file.inspect()
        self.assertEqual(out['dimensions'], [123, 91])

    def setupMne(self):
        TS = 1422522595.76096
        self.acquired = datetime.fromtimestamp(TS)
        img = Mock()
        img.info = {
            'meas_date':(TS,),
            'proj_name':'worlddom',
            'subject_info':{'first_name':'John','last_name':'Doeish'},
            'nchan':123,
            'sfreq':200}
        img.first_samp = 10
        img.last_samp = 100
        self.libs.mne.io.Raw.return_value = img
        self.libs.hasDependency.return_value = True


