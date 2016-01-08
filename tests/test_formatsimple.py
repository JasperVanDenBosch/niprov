from unittest import TestCase
from mock import Mock, sentinel, patch


class SimpleFormatTests(TestCase):

    def test_Statistics(self):
        from niprov.formatsimple import SimpleFormat
        exporter = SimpleFormat()
        out = exporter.serializeStatistics({'count':123,'totalsize':678})
        self.assertIn(' Number of files: 123', out)
        self.assertIn(' Total file size: 678', out)

    def test_Pipeline(self):
        from niprov.formatsimple import SimpleFormat
        pipeline = Mock()
        tree = {'raw.f':{'1a.f':{'2.f':{}},'1b.f':{}}}
        exp = ''
        exp += '+---raw.f\n'
        exp += '|   +---1a.f\n'
        exp += '|   |   +---2.f\n'
        exp += '|   +---1b.f\n'
        pipeline.asFilenameTree.return_value = tree
        exporter = SimpleFormat()
        out = exporter.serializePipeline(pipeline)
        self.assertEqual(exp, out)

    def test_SerializeSingle(self):
        from niprov.formatsimple import SimpleFormat
        exporter = SimpleFormat()
        out = exporter.serializeSingle(self.aFile())
        self.assertIn('a:                       b\n', out)

    def aFile(self):
        somefile = Mock()
        somefile.provenance = {'a':'b'}
        return somefile

