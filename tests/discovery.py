import unittest
from mock import Mock

class DiscoveryTests(unittest.TestCase):

    def test_one(self):
        import niprov
        log = Mock()
        filt = self.setupFilter('.x')
        os = Mock()
        os.walk.return_value = [('root',[],['/p/f1.x','/p/f2.x']),
            ('root',[],['/p/p2/f3.x'])] #(dirpath, dirnames, filenames)
        niprov.discover('root', filesys=os, listener=log, filefilter=filt)
        os.walk.assert_called_with('root')
        log.fileFound.assert_any_call('/p/f1.x')
        log.fileFound.assert_any_call('/p/f2.x')
        log.fileFound.assert_any_call('/p/p2/f3.x')

    def test_file_filters(self):
        import niprov
        log = Mock()
        os = Mock()
        filt = self.setupFilter('valid.file')
        os.walk.return_value = [('root',[],['valid.file','other.file'])]
        niprov.discover('root', filesys=os, listener=log, filefilter=filt)
        log.fileFound.assert_any_call('valid.file')
        self.assertRaises(AssertionError,
            log.fileFound.assert_any_call,'other.file')

    def setupFilter(self, valid):
        def filter_side_effect(*args):
            if valid in args[0]:
                return True
            return False
        filt = Mock()
        filt.include = Mock(side_effect=filter_side_effect)
        return filt
        

