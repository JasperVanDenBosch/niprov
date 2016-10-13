import unittest, numpy
from mock import Mock
from datetime import datetime
from tests.test_basefile import BaseFileTests


class FifTests(BaseFileTests):

    def setUp(self):
        super(FifTests, self).setUp()
        self.libs = Mock()
        self.libs.hasDependency.return_value = True
        self.libs.mne.io.read_raw_fif.side_effect = ValueError
        self.libs.mne.read_cov.side_effect = ValueError
        self.libs.mne.read_epochs.side_effect = ValueError
        self.libs.mne.read_evokeds.side_effect = ValueError
        self.libs.mne.read_forward_solution.side_effect = ValueError
        self.libs.mne.read_trans.side_effect = ValueError
        self.libs.mne.read_proj.side_effect =  ValueError
        self.dependencies.getLibraries.return_value = self.libs
        from niprov.fif import FifFile
        self.constructor = FifFile
        self.file = FifFile(self.path, dependencies=self.dependencies)

    def test_Gets_basic_info_from_mne_and_returns_it(self):
        self.setupRawFile()
        out = self.file.inspect()
        self.assertEqual(out['subject'], 'John Doeish')
        self.assertEqual(out['project'], 'worlddom')
        self.assertEqual(out['acquired'], self.acquired)

    def test_Gets_dimensions(self):
        self.setupRawFile()
        out = self.file.inspect()
        self.assertEqual(out['dimensions'], [123, 91])
        self.assertEqual(out['sampling-frequency'], 200)
        self.assertEqual(out['duration'], 91/200.)

    def test_Attach_method(self):
        self.setupRawFile()
        self.file.inspect()
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

    def test_Attach_method_doesnt_do_anything_on_non_raw_files(self):
        self.setupEpochsFile()
        self.file.getProvenance = Mock()
        self.file.attach('json')
        assert not self.libs.mne.io.read_info.called
        assert not self.file.getProvenance.called
        assert not self.libs.mne.io.write_info.called

    def test_Determines_modality(self):
        out = self.file.inspect()
        self.assertEqual(out['modality'], 'MEG')

    def test_Preserves_modality_if_inherited(self):
        pass # Doesn't have to preserve

    def test_Tries_different_mne_access_functions_or_fails_silently(self):
        out = self.file.inspect()
        self.libs.mne.io.read_raw_fif.assert_called_with(self.path, 
                                                         allow_maxshield=True)
        self.libs.mne.read_cov.assert_called_with(self.path)
        self.libs.mne.read_epochs.assert_called_with(self.path)
        self.libs.mne.read_evokeds.assert_called_with(self.path)
        self.libs.mne.read_forward_solution.assert_called_with(self.path)
        self.libs.mne.read_trans.assert_called_with(self.path)
        self.libs.mne.read_proj.assert_called_with(self.path)
        self.assertEqual(out['fif-type'], 'other')

    def test_epochs(self):
        self.setupEpochsFile()
        out = self.file.inspect()
        self.assertEqual(out['fif-type'], 'epo')
        self.assertEqual(out['lowpass'],40.0)
        self.assertEqual(out['highpass'],0.10000000149) 
        self.assertEqual(out['bad-channels'],['MEG666', 'ECG999'])
        self.assertEqual(out['dimensions'], [7, 455])

    def test_evokeds(self):
        self.setupEvokedsFile()
        out = self.file.inspect()
        self.assertEqual(out['fif-type'], 'ave')
        self.assertEqual(out['dimensions'], [3, 306, 455])

    def test_covariance(self):
        self.setupCovarianceFile()
        out = self.file.inspect()
        self.assertEqual(out['fif-type'], 'cov')
        self.assertEqual(out['dimensions'], [365, 365])

    def test_forward(self):
        self.setupForwardFile()
        out = self.file.inspect()
        self.assertEqual(out['fif-type'], 'fwd')

    def test_trans(self):
        self.setupTransFile()
        out = self.file.inspect()
        self.assertEqual(out['fif-type'], 'trans')


    def test_mnepy_read_funcs_throw_ioerror(self):
        self.libs.mne.read_trans.side_effect = IOError
        out = self.file.inspect()
        self.libs.mne.read_trans.assert_called_with(self.path)


    def setupRawFile(self):
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
        self.libs.mne.io.read_raw_fif.side_effect = None
        self.libs.mne.io.read_raw_fif.return_value = self.img
        self.libs.mne.io.read_info.return_value = self.img.info

    def setupEpochsFile(self):
        self.img = Mock()
        self.img.info = {
            'lowpass': 40.0,
            'highpass': 0.10000000149, 
            'bads': ['MEG666', 'ECG999']}
        self.img.events = numpy.zeros((7,3))
        self.img.times = numpy.zeros((455,1))
        self.libs.mne.read_epochs.side_effect = None
        self.libs.mne.read_epochs.return_value = self.img

    def setupEvokedsFile(self):
        self.img = Mock()
        self.img.info = {}
        self.img.data = numpy.zeros((306,455))
        self.libs.mne.read_evokeds.side_effect = None
        self.libs.mne.read_evokeds.return_value = [self.img, self.img, self.img]

    def setupCovarianceFile(self):
        self.img = Mock()
        self.img.data = numpy.zeros((365,365))
        self.libs.mne.read_cov.side_effect = None
        self.libs.mne.read_cov.return_value = self.img

    def setupForwardFile(self):
        self.img = Mock()
        self.libs.mne.read_forward_solution.side_effect = None
        self.libs.mne.read_forward_solution.return_value = self.img

    def setupTransFile(self):
        self.img = Mock()
        self.libs.mne.read_trans.side_effect = None
        self.libs.mne.read_trans.return_value = self.img

