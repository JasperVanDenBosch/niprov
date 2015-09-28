import unittest
from mock import Mock
import os


class FileFilterTests(unittest.TestCase):

    def test_reads_extensions_from_config(self):
        import niprov.filefilter
        dependencies = Mock()
        dependencies.getConfiguration().discover_file_extensions = ['.yes',
            '.ofc']
        filt = niprov.filefilter.FileFilter(dependencies=dependencies)
        self.assertTrue(filt.include('/p/sth.ofc'))
        self.assertTrue(filt.include('/p/sth.yes'))
        self.assertFalse(filt.include('/p/sth.nop'))


