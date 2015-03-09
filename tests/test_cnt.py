import unittest
from mock import Mock
from datetime import datetime
from tests.basefile import BaseFileTests


class CNTTests(BaseFileTests):

    def setUp(self):
        super(CNTTests, self).setUp()
        self.filesys.open.return_value = MockFile()
        from niprov.cnt import NeuroscanFile
        self.constructor = NeuroscanFile
        self.file = NeuroscanFile(self.path, listener=self.log, 
            filesystem=self.filesys, hasher=self.hasher, serializer=self.json)

    def test_Inspect_parses_experimental_basics(self):
        out = self.file.inspect()
#        self.assertEqual(out['subject'], 'John Doeish')
#        self.assertEqual(out['dimensions'], [32, 2345])
#        self.assertEqual(out['acquired'], datetime.now())
#        self.assertEqual(out['project'], 'Avalon')


class MockFile(object):

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        pass

    def read(self, nbytes):
        pass
