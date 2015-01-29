import unittest
from mock import Mock
from datetime import datetime

class InspectionTests(unittest.TestCase):

    def setUp(self):
        self.fileFactory = Mock()
        self.file = Mock()
        self.fileFactory.locatedAt.return_value = self.file

    def test_Opens_file_with_factory_and_inspects_it(self):
        import niprov.inspection
        aPath = 'example.def'
        out = niprov.inspection.inspect(aPath, file=self.fileFactory)
        self.fileFactory.locatedAt.assert_called_with(aPath)
        self.assertEqual(out, self.file.inspect())


       

