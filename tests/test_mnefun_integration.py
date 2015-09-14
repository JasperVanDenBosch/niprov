import unittest
from mock import Mock, patch


class MnefunTests(unittest.TestCase):

    def setUp(self):
        self.listener = Mock()
        self.libs = Mock()
        self.dependencies = Mock()
        self.dependencies.getListener.return_value = self.listener
        self.dependencies.getLibraries.return_value = self.libs


    def test_Discovers_fetched_raw_files(self):
        import niprov.mnefunsupport
        class MockParams(object):
            pass
        params = MockParams()
        params.work_dir = '/root'
        params.subjects = ['johndoe','janedoe']
        params.raw_dir = 'rawdir'
        def fetch_raw_files():
            pass
        with patch('niprov.mnefunsupport.discover') as discover:
            niprov.mnefunsupport.handler('Pulling raw files from acquisition machine', 
                fetch_raw_files, None, params, dependencies=self.dependencies)
            discover.assert_any_call('/root/johndoe/rawdir')
            discover.assert_any_call('/root/janedoe/rawdir')
            self.listener.mnefunEventReceived.assert_called_with('fetch_raw_files')

    def test_Logs_sss_operation(self):
        import niprov.mnefunsupport
        class MockParams(object):
            pass
        params = MockParams()
        params.subjects = ['s1','s2']
        fnames = {'raw':{'s1':['subj 1 raw file 1','subj 1 raw file 2'],
                        's2':['subj 2 raw file 1','subj 2 raw file 2']},
                'sss': {'s1':['subj 1 sss file 1','subj 1 sss file 2'],
                        's2':['subj 2 sss file 1','subj 2 sss file 2']}}
        self.libs.mnefun.get_raw_fnames.side_effect = lambda p, s, t: fnames[t][s]
        def fetch_sss_files():
            pass
        with patch('niprov.mnefunsupport.log') as log:
            niprov.mnefunsupport.handler('Pulling SSS files from remote workstation', 
                fetch_sss_files, None, params, dependencies=self.dependencies)
            log.assert_any_call(fnames['sss']['s1'][0],
                                'Signal Space Separation',
                                fnames['raw']['s1'][0], provenance = {'mnefun':{}})
            log.assert_any_call(fnames['sss']['s2'][1],
                                'Signal Space Separation',
                                fnames['raw']['s2'][1], provenance = {'mnefun':{}})

    def test_Logs_ssp_operation(self):
        import niprov.mnefunsupport
        class MockParams(object):
            pass
        params = MockParams()
        params.subjects = ['s1','s2']
        fnames = {'pca':{'s1':['subj 1 pca file 1','subj 1 pca file 2'],
                        's2':['subj 2 pca file 1','subj 2 pca file 2']},
                'sss': {'s1':['subj 1 sss file 1','subj 1 sss file 2'],
                        's2':['subj 2 sss file 1','subj 2 sss file 2']}}
        self.libs.mnefun.get_raw_fnames.side_effect = lambda p, s, t: fnames[t][s]
        def apply_preprocessing_combined():
            pass
        with patch('niprov.mnefunsupport.log') as log:
            niprov.mnefunsupport.handler('Apply SSP vectors and filtering.', 
                apply_preprocessing_combined, None, params, 
                dependencies=self.dependencies)
            log.assert_any_call(fnames['pca']['s1'][0],
                                'Signal Space Projection',
                                fnames['sss']['s1'][0], provenance = {'mnefun':{}})
            log.assert_any_call(fnames['pca']['s2'][1],
                                'Signal Space Projection',
                                fnames['sss']['s2'][1], provenance = {'mnefun':{}})

    def test_Logs_epoch_operation(self):
        import niprov.mnefunsupport
        class MockParams(object):
            pass
        params = MockParams()
        params.subjects = ['s1','s2']
        params.analyses = ['a']
        fnames = {'pca':{'s1':['subj 1 pca file 1','subj 1 pca file 2'],
                        's2':['subj 2 pca file 1','subj 2 pca file 2']}}
        epochfnames = {'s1':['s1 evt 1','s1 evt 2','s1 evt 3'],
                        's2':['s2 evt 1','s2 evt 2','s2 evt 3']}
        self.libs.mnefun.get_raw_fnames.side_effect = \
            lambda p, s, t: fnames[t][s]
        self.libs.mnefun._paths.get_epochs_evokeds_fnames.side_effect = \
            lambda p, s, a: epochfnames[s]
        def save_epochs():
            pass
        with patch('niprov.mnefunsupport.log') as log:
            niprov.mnefunsupport.handler('Doing epoch EQ/DQ', 
                save_epochs, None, params, dependencies=self.dependencies)
            log.assert_any_call(epochfnames['s1'][0], #any event file
                                'Epoching',
                                fnames['pca']['s1'], provenance = {'mnefun':{}}) #all raw files for subj
            log.assert_any_call(epochfnames['s2'][1], #any event file
                                'Epoching',
                                fnames['pca']['s2'], provenance = {'mnefun':{}}) #all raw files for subj

    def test_Log_seeded_with_params_based_custom_provenance(self):
        import niprov.mnefunsupport
        class MockParams(object):
            pass
        params = MockParams()
        params.tmin = -0.2
        params.quat_tol = 5e-2
        params.subjects = ['s1','s2']
        fnames = {'raw':{'s1':['subj 1 raw file 1','subj 1 raw file 2'],
                        's2':['subj 2 raw file 1','subj 2 raw file 2']},
                'sss': {'s1':['subj 1 sss file 1','subj 1 sss file 2'],
                        's2':['subj 2 sss file 1','subj 2 sss file 2']}}
        self.libs.mnefun.get_raw_fnames.side_effect = lambda p, s, t: fnames[t][s]
        def fetch_sss_files():
            pass
        with patch('niprov.mnefunsupport.log') as log:
            niprov.mnefunsupport.handler('Pulling SSS files from remote workstation', 
                fetch_sss_files, None, params, dependencies=self.dependencies)
            log.assert_called_with(fnames['sss']['s2'][1],
                                'Signal Space Separation',
                                fnames['raw']['s2'][1], 
                                provenance={'mnefun':{
                                    'tmin':-0.2,
                                    'quat_tol':5e-2}})


#    write_epochs : bool
#        Write epochs to disk.
#    gen_covs : bool
#        Generate covariances.
#    gen_fwd : bool
#        Generate forward solutions.
#    get_inv : bool
#        Generate inverses.
#    gen_report : bool
#        Generate HTML reports.

