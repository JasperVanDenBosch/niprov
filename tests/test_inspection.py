import unittest
from mock import Mock
from datetime import datetime

class InspectionTests(unittest.TestCase):

    def setUp(self):
        self.fileFactory = Mock()
        self.file = Mock()
        self.fileFactory.locatedAt.return_value = self.file
        self.dependencies = Mock()
        self.dependencies.getFileFactory.return_value = self.fileFactory

    def test_Opens_file_with_factory_and_inspects_it(self):
        import niprov.inspection
        aPath = 'example.def'
        out = niprov.inspection.inspect(aPath, dependencies=self.dependencies)
        self.fileFactory.locatedAt.assert_called_with(aPath)
        self.assertEqual(out, self.file.inspect())


       

