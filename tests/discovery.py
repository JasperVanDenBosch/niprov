import unittest
from mock import Mock

class DiscoveryTests(unittest.TestCase):

    def test_one(self):
        import niprov
        log = Mock()
        os = Mock()
        os.glob.return_value = ['/p/f1.x','/p/p2/f2.x']
        niprov.discover('target_root_dir', filesys=os, listener=log)
        os.glob.assert_called_with('target_root_dir')
        log.fileFound.assert_any_call('/p/f1.x')
        log.fileFound.assert_any_call('/p/p2/f2.x')
        
