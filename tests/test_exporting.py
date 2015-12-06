from mock import Mock, patch, sentinel
from tests.ditest import DependencyInjectionTestBase


class ExportingTest(DependencyInjectionTestBase):

    def setUp(self):
        super(ExportingTest, self).setUp()

    def test_export(self):
        import niprov.exporting 
        self.repo.all.return_value = [sentinel.p1, sentinel.p2]
        niprov.exporting.JsonFile = self.patchJsonFileConstructor()
        niprov.exporting.export(dependencies=self.dependencies)
        assert self.JsonFileCtr.called, "Did not create a JsonFile repo."
        urlUsed = self.tempRepo.dependencies.getConfiguration().database_url
        self.assertEqual(urlUsed, 'provenance.json')
        self.tempRepo.add.assert_any_call(sentinel.p1)
        self.tempRepo.add.assert_any_call(sentinel.p2)

    def patchJsonFileConstructor(self):
        self.tempRepo = Mock()
        self.JsonFileCtr = Mock()
        def ctr(dependencies): 
            self.tempRepo.dependencies = dependencies
            return self.tempRepo
        self.JsonFileCtr.side_effect = ctr
        return self.JsonFileCtr



