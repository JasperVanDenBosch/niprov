import unittest
from mock import Mock
import os




class FileFilterTests(unittest.TestCase):

    def test_reads_extensions_from_default_file(self):
        packageroot = os.path.split(os.path.split(__file__)[0])[0]
        defaultfilterfile = os.path.join(packageroot,'discovery-filter.txt')
        from niprov.filefilter import FileFilter
        filesys = Mock()
        filesys.readlines.return_value = ['.abc','.def']
        filt = FileFilter(filesys=filesys)
        filesys.readlines.assert_called_with(defaultfilterfile)
        self.assertTrue(filt.include('/p/sth.abc'))
        self.assertTrue(filt.include('/p/sth.def'))
        self.assertFalse(filt.include('/p/sth.xyz'))


