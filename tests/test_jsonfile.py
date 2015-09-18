from mock import Mock
from tests.ditest import DependencyInjectionTestBase


class JsonFileTest(DependencyInjectionTestBase):

    def setUp(self):
        super(JsonFileTest, self).setUp()
        self.dependencies.getConfiguration().database_url = ''

    def test_Update(self):
        from niprov.jsonfile import JsonFile
        repo = JsonFile(self.dependencies)
        repo.all = Mock()
        repo.all.return_value = [{'location':'1','path':'a'},
            {'location':'2','path':'b'}]
        image = Mock()
        image.location.toString.return_value = '2'
        image.provenance = {'foo':'bar'}
        repo.update(image)
        self.serializer.serializeList.assert_called_with(
            [{'location':'1','path':'a'},{'foo':'bar'}])
        self.filesys.write.assert_called_with(repo.datafile, 
            self.serializer.serializeList())

