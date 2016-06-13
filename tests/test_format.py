from mock import Mock, sentinel
from tests.ditest import DependencyInjectionTestBase


class FormatTests(DependencyInjectionTestBase):

    def test_If_serialize_called_with_list_calls_serializeList(self):
        from niprov.format import Format
        exp = Format()
        exp.serializeList = Mock()
        out = exp.serialize([sentinel.p1, sentinel.p2])
        exp.serializeList.assert_called_with([sentinel.p1, sentinel.p2])
        self.assertEqual(out, exp.serializeList())

    def test_If_serialize_called_with_item_calls_serializeSingle(self):
        from niprov.format import Format
        exp = Format()
        exp.serializeSingle = Mock()
        out = exp.serialize(sentinel.p1)
        exp.serializeSingle.assert_called_with(sentinel.p1)
        self.assertEqual(out, exp.serializeSingle())

    def test_If_called_with_dict_calls_serializeStatistics(self):
        from niprov.format import Format
        exp = Format()
        exp.serializeStatistics = Mock()
        out = exp.serialize({'a':'b'})
        exp.serializeStatistics.assert_called_with({'a':'b'})
        self.assertEqual(out, exp.serializeStatistics())

    def test_If_created_with_pipeline_calls_serializePipeline(self):
        from niprov.format import Format
        from niprov.pipeline import Pipeline
        exp = Format(dependencies=self.dependencies)
        exp.serializePipeline = Mock()
        pipe = Pipeline([])
        out = exp.serialize(pipe)
        #self.pipelineFactory.forFile.assert_called_with(img)
        exp.serializePipeline.assert_called_with(pipe)
        self.assertEqual(out, exp.serializePipeline())

    def test_If_created_with_iterable_calls_serializeList(self):
        from niprov.format import Format
        exp = Format()
        exp.serializeList = Mock()
        exp.serializeSingle = Mock()
        class MockQuery(object):
            def __iter__(self):
                pass
        query = MockQuery()
        out = exp.serialize(query)
        exp.serializeList.assert_called_with(query)
        self.assertEqual(out, exp.serializeList())

