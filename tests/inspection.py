import unittest
from mock import Mock

class InspectionTests(unittest.TestCase):

    def test_Loads_file_with_nibabel(self):
        import niprov.inspection
        log = Mock()
        libs = Mock()
        libs.hasDependency.return_value = True
        niprov.inspection.inspect('/p/f1.x', listener=log, libs=libs)
        libs.nibabel.load.assert_any_call('/p/f1.x')

    def test_Doesnt_use_nibabel_if_not_installed(self):
        import niprov.inspection
        log = Mock()
        libs = Mock()
        libs.hasDependency.return_value = False
        niprov.inspection.inspect('/p/f1.x', listener=log, libs=libs)
        self.assertRaises(AssertionError,
            libs.nibabel.load.assert_any_call, '/p/f1.x')
