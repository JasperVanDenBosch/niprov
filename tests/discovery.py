import unittest
from mock import Mock

class DiscoveryTests(unittest.TestCase):

    def test_one(self):
        import niprov
        log = Mock()
        os = Mock()
        os.walk.return_value = [('root',[],['/p/f1.x','/p/f2.x']),
            ('root',[],['/p/p2/f3.x'])] #(dirpath, dirnames, filenames)
        niprov.discover('root', filesys=os, listener=log)
        os.walk.assert_called_with('root')
        log.fileFound.assert_any_call('/p/f1.x')
        log.fileFound.assert_any_call('/p/f2.x')
        log.fileFound.assert_any_call('/p/p2/f3.x')
        
