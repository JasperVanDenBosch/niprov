import unittest
import mock
from mock import Mock
import os.path as ospath

class DiscoveryTests(unittest.TestCase):

    def setUp(self):
        self.filesys = Mock()
        self.filesys.walk.return_value = [('root',[],['known','new','unknown'])]
        self.listener = Mock()
        self.filt = Mock()
        self.add = Mock()
        self.add.return_value = (Mock(), 'new')
        self.dependencies = Mock()
        self.dependencies.getFilesystem.return_value = self.filesys
        self.dependencies.getListener.return_value = self.listener
        self.dependencies.getFileFilter.return_value = self.filt

    def discover(self, path):
        import niprov.discovery
        niprov.discovery.add = self.add
        niprov.discovery.discover(path, dependencies=self.dependencies)

    def test_Calls_add_on_files_encountered(self):
        self.setupFilter('.x')
        self.filesys.walk.return_value = [('root',[],['p/f1.x','p/f2.x']),
            ('root',[],['p/p2/f3.x'])] #(dirpath, dirnames, filenames)
        self.discover('root')
        self.filesys.walk.assert_called_with('root')
        self.add.assert_any_call('root/p/f1.x', transient=False, dependencies=self.dependencies)
        self.add.assert_any_call('root/p/f2.x', transient=False, dependencies=self.dependencies)
        self.add.assert_any_call('root/p/p2/f3.x', transient=False, dependencies=self.dependencies)

    def test_file_filters(self):
        self.setupFilter('valid.file')
        self.filesys.walk.return_value = [('root',[],['valid.file','other.file'])]
        self.discover('root')
        self.add.assert_any_call('root/valid.file', transient=False, dependencies=self.dependencies)
        self.assertNotCalledWith(self.add, 'root/other.file')

    def test_Gives_listener_summary(self):
        self.filesys.walk.return_value = [('root',[],['a','b','c','d','e','f','g','h'])]
        a,b,c,d,e,f,g,h = [(Mock(), s) for s in ['new','new','series','series',
            'series','failed','known','known']]
        self.add.side_effect = [a,b,c,d,e,f,g,h]
        self.discover('root')
        self.listener.discoveryFinished.assert_called_with(nnew=2, nadded=3, nfailed=1, ntotal=8)

    def assertNotCalledWith(self, m, *args, **kwargs):
        c = mock.call(*args, **kwargs)
        assert c not in m.call_args_list, "Unexpectedly found call: "+str(c)

    def setupFilter(self, valid):
        def filter_side_effect(*args):
            if valid in args[0]:
                return True
            return False
        self.filt.include = Mock(side_effect=filter_side_effect)
        

