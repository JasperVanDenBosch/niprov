import unittest
import mock
from mock import Mock
import os.path as ospath

class DiscoveryTests(unittest.TestCase):

    def setUp(self):
        self.repo = Mock()
        self.repo.knowsByPath.return_value = False
        self.filesys = Mock()
        self.listener = Mock()
        self.filt = Mock()
        self.inspect = Mock()
        self.inspect.side_effect = lambda x: ('p', x)

    def discover(self, path):
        import niprov.discovery
        niprov.discovery.inspect = self.inspect
        niprov.discovery.discover(path, filesys=self.filesys, listener=self.listener,
            filefilter=self.filt, repository=self.repo)

    def test_Tells_listener_about_files_found(self):
        self.setupFilter('.x')
        self.filesys.walk.return_value = [('root',[],['/p/f1.x','/p/f2.x']),
            ('root',[],['/p/p2/f3.x'])] #(dirpath, dirnames, filenames)
        self.discover('root')
        self.filesys.walk.assert_called_with('root')
        self.listener.fileFound.assert_any_call('/p/f1.x', self.inspect('/p/f1.x'))
        self.listener.fileFound.assert_any_call('/p/f2.x', self.inspect('/p/f2.x'))
        self.listener.fileFound.assert_any_call('/p/p2/f3.x', self.inspect('/p/p2/f3.x'))

    def test_file_filters(self):
        self.setupFilter('valid.file')
        self.filesys.walk.return_value = [('root',[],['valid.file','other.file'])]
        self.discover('root')
        self.listener.fileFound.assert_any_call('valid.file', 
            self.inspect('root/valid.file'))
        self.assertRaises(AssertionError,
            self.listener.fileFound.assert_any_call,'other.file', 
                self.inspect('root/other.file'))

    def test_Calls_inspect(self):
        self.setupFilter('.valid')
        self.filesys.walk.return_value = [('root',[],['a.valid','other.file','b.valid'])]
        self.discover('root')
        self.inspect.assert_any_call(ospath.join('root','a.valid'))
        self.inspect.assert_any_call(ospath.join('root','b.valid'))

    def test_If_inspect_returns_no_provenance_dont_call_fileFound(self):
        self.setupFilter('valid.file')
        self.filesys.walk.return_value = [('root',[],['valid.file','other.file'])]
        self.discover('root')
        self.assertRaises(AssertionError,
            self.listener.fileFound.assert_any_call,'valid.file', self.inspect('valid.file'))

    def test_Hands_provenance_to_repository(self):
        self.setupFilter('.valid')
        self.filesys.walk.return_value = [('root',[],['a.valid','other.file','b.valid'])]
        self.discover('root')
        self.repo.add.assert_any_call(('p', 'root/a.valid'))
        self.repo.add.assert_any_call(('p', 'root/b.valid'))

    def test_If_discovers_file_that_is_known_ignore_it(self):
        self.repo.knowsByPath.side_effect = lambda p: True if p == 'root/known' else False
        self.filesys.walk.return_value = [('root',[],['known','new','unknown'])]
        self.discover('root')
        self.repo.add.assert_any_call(('p', 'root/unknown'))
        self.assertNotCalledWith(self.repo.add, ('p', 'root/known'))
        self.listener.knownFile.assert_called_with('root/known')

    def assertNotCalledWith(self, m, *args, **kwargs):
        c = mock.call(*args, **kwargs)
        assert c not in m.call_args_list, "Unexpectedly found call: "+str(c)


    def setupFilter(self, valid):
        def filter_side_effect(*args):
            if valid in args[0]:
                return True
            return False
        self.filt.include = Mock(side_effect=filter_side_effect)
        

