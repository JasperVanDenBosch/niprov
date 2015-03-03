import unittest
from mock import Mock
import os


class FileFilterTests(unittest.TestCase):

    def test_reads_extensions_from_default_file(self):
        import niprov.filefilter
        filesys = Mock()
        filesys.readlines.return_value = ['.abc','.def']
        niprov.filefilter.pkg_resources = Mock()
        filt = niprov.filefilter.FileFilter(filesys=filesys)
        niprov.filefilter.pkg_resources.resource_filename.assert_called_with(
            'niprov','discovery-filter.txt')
        filesys.readlines.assert_called_with(
            niprov.filefilter.pkg_resources.resource_filename())
        self.assertTrue(filt.include('/p/sth.abc'))
        self.assertTrue(filt.include('/p/sth.def'))
        self.assertFalse(filt.include('/p/sth.xyz'))


