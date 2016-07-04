import unittest
from mock import Mock
from datetime import datetime
from tests.test_basefile import BaseFileTests


class FifTests(BaseFileTests):

    def setUp(self):
        super(FifTests, self).setUp()
        self.libs = Mock()
        self.dependencies.getLibraries.return_value = self.libs
        self.setupMne()
        from niprov.fif import FifFile
        self.constructor = FifFile
        self.file = FifFile(self.path, dependencies=self.dependencies)

    def test_Gets_basic_info_from_mne_and_returns_it(self):
        out = self.file.inspect()
        self.assertEqual(out['subject'], 'John Doeish')
        self.assertEqual(out['project'], 'worlddom')
        self.assertEqual(out['acquired'], self.acquired)

    def test_Gets_dimensions(self):
        out = self.file.inspect()
        self.assertEqual(out['dimensions'], [123, 91])
        self.assertEqual(out['sampling-frequency'], 200)
        self.assertEqual(out['duration'], 91/200.)

    def test_Attach_method(self):
        self.file.getProvenance = Mock()
        self.file.getProvenance.return_value = 'serial prov'
        self.file.attach('json')
        self.file.getProvenance.assert_called_with('json')
        self.assertIn('existing bla bla ', #original string+added space 
            self.img.info['description'])
        self.assertIn('NIPROV:'+'serial prov', 
            self.img.info['description'])
        self.libs.mne.io.write_info.assert_called_with(self.file.path, 
            self.img.info)

    def test_Determines_modality(self):
        out = self.file.inspect()
        self.assertEqual(out['modality'], 'MEG')

    def test_Preserves_modality_if_inherited(self):
        pass # Doesn't have to preserve

    def setupMne(self):
        TS = 1422522595.76096
        self.acquired = datetime.fromtimestamp(TS)
        self.img = Mock()
        self.img.info = {
            'meas_date':(TS,),
            'proj_name':'worlddom',
            'subject_info':{'first_name':'John','last_name':'Doeish'},
            'nchan':123,
            'sfreq':200,
            'description':'existing bla bla'}
        self.img.first_samp = 10
        self.img.last_samp = 100
        self.libs.mne.io.Raw.return_value = self.img
        self.libs.mne.io.read_info.return_value = self.img.info
        self.libs.hasDependency.return_value = True



