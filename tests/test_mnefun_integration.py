import unittest
from mock import Mock, patch


class MnefunTests(unittest.TestCase):

    def setUp(self):
        self.listener = Mock()
        self.libs = Mock()

    def test_Discovers_fetched_raw_files(self):
        import niprov.mnefunsupport
        params = Mock()
        params.work_dir = '/root'
        params.subjects = ['johndoe','janedoe']
        params.raw_dir = 'rawdir'
        def fetch_raw_files():
            pass
        with patch('niprov.mnefunsupport.discover') as discover:
            niprov.mnefunsupport.handler('Pulling raw files from acquisition machine', 
                fetch_raw_files, None, params, listener=self.listener)
            discover.assert_any_call('/root/johndoe/rawdir')
            discover.assert_any_call('/root/janedoe/rawdir')
            self.listener.mnefunEventReceived.assert_called_with('fetch_raw_files')

    def test_Logs_sss_operation(self):
        import niprov.mnefunsupport
        params = Mock()
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
                fetch_sss_files, None, params, listener=self.listener, libs=self.libs)
            log.assert_any_call(fnames['sss']['s1'][0],
                                'Signal Space Separation',
                                fnames['raw']['s1'][0])
            log.assert_any_call(fnames['sss']['s2'][1],
                                'Signal Space Separation',
                                fnames['raw']['s2'][1])

    def test_Logs_ssp_operation(self):
        import niprov.mnefunsupport
        params = Mock()
        params.subjects = ['s1','s2']
        fnames = {'pca':{'s1':['subj 1 pca file 1','subj 1 pca file 2'],
                        's2':['subj 2 pca file 1','subj 2 pca file 2']},
                'sss': {'s1':['subj 1 sss file 1','subj 1 sss file 2'],
                        's2':['subj 2 sss file 1','subj 2 sss file 2']}}
        self.libs.mnefun.get_raw_fnames.side_effect = lambda p, s, t: fnames[t][s]
        def apply_ssp():
            pass
        with patch('niprov.mnefunsupport.log') as log:
            niprov.mnefunsupport.handler('Apply SSP vectors and filtering.', 
                apply_ssp, None, params, listener=self.listener, libs=self.libs)
            log.assert_any_call(fnames['pca']['s1'][0],
                                'Signal Space Projection',
                                fnames['sss']['s1'][0])
            log.assert_any_call(fnames['pca']['s2'][1],
                                'Signal Space Projection',
                                fnames['sss']['s2'][1])

#new, 
#transformation, 
#parents, 
#code=None, 
#logtext=None, 
#transient=False,
#script=None, 
#provenance=None

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

