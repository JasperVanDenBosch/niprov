from tests.ditest import DependencyInjectionTestBase
from mock import Mock


class DictFormatTests(DependencyInjectionTestBase):

    def setUp(self):
        super(DictFormatTests, self).setUp()

    def test_serialize_item_returns_its_prov(self):
        from niprov.formatdict import DictFormat
        form = DictFormat(self.dependencies)
        out = form.serializeSingle(self.aFile())
        self.assertEqual({'a':'b'}, out)

    def test_serialize_list_returns_its_provs(self):
        from niprov.formatdict import DictFormat
        form = DictFormat(self.dependencies)
        out = form.serializeList([self.aFile(), self.aFile(), self.aFile()])
        self.assertEqual([{'a':'b'},{'a':'b'},{'a':'b'}], out)

    def aFile(self):
        somefile = Mock()
        somefile.provenance = {'a':'b'}
        return somefile
