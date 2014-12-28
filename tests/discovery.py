import unittest
from mock import Mock
import os.path as ospath

class DiscoveryTests(unittest.TestCase):

    def test_Tells_listener_about_files_found(self):
        import niprov.discovery
        niprov.discovery.inspect = Mock()
        log = Mock()
        filt = self.setupFilter('.x')
        os = Mock()
        os.walk.return_value = [('root',[],['/p/f1.x','/p/f2.x']),
            ('root',[],['/p/p2/f3.x'])] #(dirpath, dirnames, filenames)
        niprov.discovery.discover('root', filesys=os, listener=log, 
            filefilter=filt, repository=Mock())
        os.walk.assert_called_with('root')
        log.fileFound.assert_any_call('/p/f1.x', niprov.discovery.inspect())
        log.fileFound.assert_any_call('/p/f2.x', niprov.discovery.inspect())
        log.fileFound.assert_any_call('/p/p2/f3.x', niprov.discovery.inspect())

    def test_file_filters(self):
        import niprov.discovery
        niprov.discovery.inspect = Mock()
        log = Mock()
        os = Mock()
        filt = self.setupFilter('valid.file')
        os.walk.return_value = [('root',[],['valid.file','other.file'])]
        niprov.discovery.discover('root', filesys=os, listener=log,
            filefilter=filt, repository=Mock())
        log.fileFound.assert_any_call('valid.file', niprov.discovery.inspect())
        self.assertRaises(AssertionError,
            log.fileFound.assert_any_call,'other.file', niprov.discovery.inspect())

    def test_Calls_inspect(self):
        import niprov.discovery
        niprov.discovery.inspect = Mock()
        log = Mock()
        os = Mock()
        filt = self.setupFilter('.valid')
        os.walk.return_value = [('root',[],['a.valid','other.file','b.valid'])]
        niprov.discovery.discover('root', filesys=os, listener=log,
            filefilter=filt, repository=Mock())
        niprov.discovery.inspect.assert_any_call(ospath.join('root','a.valid'))
        niprov.discovery.inspect.assert_any_call(ospath.join('root','b.valid'))

    def test_If_inspect_returns_no_provenance_dont_call_fileFound(self):
        import niprov.discovery
        niprov.discovery.inspect = Mock()
        niprov.discovery.inspect.return_value = None
        log = Mock()
        os = Mock()
        filt = self.setupFilter('valid.file')
        os.walk.return_value = [('root',[],['valid.file','other.file'])]
        niprov.discovery.discover('root', filesys=os, listener=log,
            filefilter=filt, repository=Mock())
        self.assertRaises(AssertionError,
            log.fileFound.assert_any_call,'valid.file', niprov.discovery.inspect())

    def test_Hands_provenance_to_repository(self):
        import niprov.discovery
        niprov.discovery.inspect = Mock()
        niprov.discovery.inspect.side_effect = lambda x: ('p', x)
        os = Mock()
        repo = Mock()
        filt = self.setupFilter('.valid')
        os.walk.return_value = [('root',[],['a.valid','other.file','b.valid'])]
        niprov.discovery.discover('root', filesys=os, listener=Mock(),
            filefilter=filt, repository=repo)
        repo.store.assert_any_call([('p', 'root/a.valid'), ('p', 'root/b.valid')])



    def setupFilter(self, valid):
        def filter_side_effect(*args):
            if valid in args[0]:
                return True
            return False
        filt = Mock()
        filt.include = Mock(side_effect=filter_side_effect)
        return filt
        

