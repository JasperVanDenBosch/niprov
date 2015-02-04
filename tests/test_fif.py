import unittest
from mock import Mock
from datetime import datetime
from tests.basefile import BasicInspectionTests


class FifTests(BasicInspectionTests):

    def setUp(self):
        super(FifTests, self).setUp()
        self.libs = Mock()
        self.setupMne()
        from niprov.fif import FifFile
        self.file = FifFile(self.path, listener=self.log, 
            filesystem=self.filesys, hasher=self.hasher, dependencies=self.libs,
            serializer=self.json)

    def test_If_error_during_inspection_tells_listener_and_returns_None(self):
        self.libs.mne.io.Raw.side_effect = ValueError
        out = self.file.inspect()
        self.log.fileError.assert_called_with(self.path)

    def test_Gets_basic_info_from_mne_and_returns_it(self):
        out = self.file.inspect()
        self.assertEqual(out['subject'], 'John Doeish')
        self.assertEqual(out['project'], 'worlddom')
        self.assertEqual(out['acquired'], self.acquired)

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
        self.libs.mne.io.Raw.return_value = img
        self.libs.hasDependency.return_value = True


