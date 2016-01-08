from mock import Mock, patch, sentinel
from tests.ditest import DependencyInjectionTestBase
from datetime import datetime


class ExportingTest(DependencyInjectionTestBase):

    def setUp(self):
        super(ExportingTest, self).setUp()
        self.tempRepo = Mock()

    def test_import(self):
        import niprov.exporting 
        self.tempRepo.all.return_value = [sentinel.p1, sentinel.p2]
        niprov.exporting.JsonFile = self.patchJsonFileConstructor()
        niprov.exporting.importp('target_file', dependencies=self.dependencies)
        assert self.JsonFileCtr.called, "Did not create a JsonFile repo."
        urlUsed = self.tempRepo.dependencies.getConfiguration().database_url
        self.assertEqual(urlUsed, 'target_file')
        self.repo.add.assert_any_call(sentinel.p1)
        self.repo.add.assert_any_call(sentinel.p2)

    def patchJsonFileConstructor(self):
        self.JsonFileCtr = Mock()
        def ctr(dependencies): 
            self.tempRepo.dependencies = dependencies
            return self.tempRepo
        self.JsonFileCtr.side_effect = ctr
        return self.JsonFileCtr



