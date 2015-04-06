import unittest
from mock import Mock, patch

class MnefunTests(unittest.TestCase):

    def setUp(self):
        pass

    def test_Discovers_fetched_raw_files(self):
        import niprov.mnefun
        p = Mock()
        p.work_dir = '/root'
        p.subjects = ['johndoe','janedoe']
        p.raw_dir = 'rawdir'
        with patch('niprov.mnefun.discover') as discover:
            niprov.mnefun.handler('Pulling raw files from acquisition machine', 
                None, None, p)
            discover.assert_any_call('/root/johndoe/rawdir')
            discover.assert_any_call('/root/janedoe/rawdir')

#    def test_Logs_sss_operation(self):
#        import niprov.mnefun
#        with patch('niprov.mnefun.log') as log:
#            niprov.mnefun.handler('Doing epoch EQ/DQ', None, None, None)
#            log.assert_called_with()

#new, 
#transformation, 
#parents, 
#code=None, 
#logtext=None, 
#transient=False,
#script=None, 
#provenance=None

#    fetch_raw : bool
#        Fetch raw recording files from acquisition machine.

#    fetch_sss : bool
#        Fetch SSS files from SSS workstation.


#    gen_ssp : bool
#        Generate SSP vectors.
#    apply_ssp : bool
#        Apply SSP vectors and filtering.
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

