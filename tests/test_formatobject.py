from tests.ditest import DependencyInjectionTestBase
from mock import Mock


class ObjectFormatTests(DependencyInjectionTestBase):

    def setUp(self):
        super(ObjectFormatTests, self).setUp()

    def test_serialize_item_returns_itself(self):
        from niprov.formatobject import ObjectFormat
        form = ObjectFormat(self.dependencies)
        item = self.aFile()
        out = form.serializeSingle(item)
        self.assertEqual(item, out)

    def test_serialize_list_returns_itself(self):
        from niprov.formatobject import ObjectFormat
        form = ObjectFormat(self.dependencies)
        mylist = [self.aFile(), self.aFile(), self.aFile()]
        out = form.serializeList(mylist)
        self.assertEqual(mylist, out)

    def test_serialize_stats_returns_itself(self):
        from niprov.formatobject import ObjectFormat
        form = ObjectFormat(self.dependencies)
        stats = {'pval':'0.05'}
        out = form.serializeStatistics(stats)
        self.assertEqual(stats, out)

    def test_serialize_pipeline_returns_itself(self):
        from niprov.formatobject import ObjectFormat
        from niprov.pipeline import Pipeline
        form = ObjectFormat(self.dependencies)
        pipe = Pipeline([])
        out = form.serializePipeline(pipe)
        self.assertEqual(pipe, out)

    def aFile(self):
        somefile = Mock()
        somefile.provenance = {'a':'b'}
        return somefile
