from mock import Mock
from tests.ditest import DependencyInjectionTestBase
import datetime, random


class JsonFileTest(DependencyInjectionTestBase):

    def setUp(self):
        super(JsonFileTest, self).setUp()
        self.dependencies.getConfiguration().database_url = ''

    def imageWithProvenance(self, prov):
        img = Mock()
        img.provenance = prov
        if 'location' in prov:
            img.location.toString.return_value = prov['location']
        return img

    def test_Add(self):
        from niprov.jsonfile import JsonFile
        repo = JsonFile(self.dependencies)
        img1 = self.imageWithProvenance({'location':'1','foo':'baz'})
        repo.all = Mock()
        repo.all.return_value = [img1]
        image = self.imageWithProvenance({'location': '2','foo':'bar'})
        repo.add(image)
        self.serializer.serializeList.assert_called_with(
            [img1, image])
        self.filesys.write.assert_called_with(repo.datafile, 
            self.serializer.serializeList())

    def test_Update(self):
        from niprov.jsonfile import JsonFile
        repo = JsonFile(self.dependencies)
        img1 = self.imageWithProvenance({'location':'1','path':'a'})
        img2 = self.imageWithProvenance({'location':'2','path':'b'})
        repo.all = Mock()
        repo.all.return_value = [img1, img2]
        image = self.imageWithProvenance({'location': '2','foo':'bar'})
        repo.update(image)
        self.serializer.serializeList.assert_called_with(
            [img1,image])
        self.filesys.write.assert_called_with(repo.datafile, 
            self.serializer.serializeList())

    def test_knowsByLocation(self):
        from niprov.jsonfile import JsonFile
        repo = JsonFile(self.dependencies)
        repo.byLocation = Mock()
        self.assertTrue(repo.knowsByLocation(''))
        repo.byLocation.side_effect = IndexError
        self.assertFalse(repo.knowsByLocation(''))

    def test_byLocation(self):
        from niprov.jsonfile import JsonFile
        repo = JsonFile(self.dependencies)
        img1 = self.imageWithProvenance({'location':'1','path':'a'})
        img2 = self.imageWithProvenance({'location':'2','path':'b'})
        repo.all = Mock()
        repo.all.return_value = [img1, img2]
        out = repo.byLocation('2')
        self.assertEqual(img2, out)

    def test_byLocation_works_for_file_in_series(self):
        from niprov.jsonfile import JsonFile
        repo = JsonFile(self.dependencies)
        img1 = self.imageWithProvenance({'location':'1','path':'a'})
        img3 = self.imageWithProvenance({'location':'3','filesInSeries':['boo','bah']})
        repo.all = Mock()
        repo.all.return_value = [img1, img3]
        out = repo.byLocation('boo')
        self.assertEqual(img3, out)

    def test_updateApproval(self):
        from niprov.jsonfile import JsonFile
        repo = JsonFile(self.dependencies)
        img = Mock()
        img.provenance = {'fiz':'baf','approval':'notsure'}
        def assertion(img):
            self.assertEqual({'fiz':'baf','approval':'excellent!'}, img.provenance)
        repo.byLocation = Mock()
        repo.byLocation.return_value = img
        repo.update = Mock()
        repo.update.side_effect = assertion
        repo.updateApproval('/p/f1','excellent!')

    def test_bySubject(self):
        from niprov.jsonfile import JsonFile
        repo = JsonFile(self.dependencies)
        img1 = self.imageWithProvenance({'subject':'john','a':'b'})
        img2 = self.imageWithProvenance({'subject':'tim','a':'d'})
        img3 = self.imageWithProvenance({'subject':'john','a':'f'})
        repo.all = Mock()
        repo.all.return_value = [img1, img2, img3]
        out = repo.bySubject('john')
        self.assertEqual([img1, img3], out)

    def test_byApproval(self):
        from niprov.jsonfile import JsonFile
        repo = JsonFile(self.dependencies)
        img1 = self.imageWithProvenance({'approval':'y','a':'b'})
        img2 = self.imageWithProvenance({'approval':'x','a':'d'})
        img3 = self.imageWithProvenance({'approval':'x','a':'f'})
        repo.all = Mock()
        repo.all.return_value = [img1, img2, img3]
        out = repo.byApproval('x')
        self.assertEqual([img2, img3], out)

    def test_latest(self):
        from niprov.jsonfile import JsonFile
        repo = JsonFile(self.dependencies)
        img1 = self.imageWithProvenance({'added':datetime.datetime(1982, 1, 5)})
        img2 = self.imageWithProvenance({'added':datetime.datetime(1982, 2, 5)})
        img3 = self.imageWithProvenance({'added':datetime.datetime(1982, 3, 5)})
        img4 = self.imageWithProvenance({'added':datetime.datetime(1982, 4, 5)})
        img5 = self.imageWithProvenance({'added':datetime.datetime(1982, 5, 5)})
        repo.all = Mock()
        repo.all.return_value = [img1,img2,img3,img4,img5]
        out = repo.latest(3)
        self.assertEqual([img5, img4, img3], out)

    def test_stats(self):
        from niprov.jsonfile import JsonFile
        repo = JsonFile(self.dependencies)
        repo.all = Mock()
        records = [{},{},{},{},{},{},{},{},{},{},{}]
        totalsize = 0
        for r in records:
            r['size'] = random.randint(1,1000)
            totalsize += r['size']
        repo.all.return_value = [self.imageWithProvenance(r) for r in records]
        out = repo.statistics()
        self.assertEqual(11, out['count'])
        self.assertEqual(totalsize, out['totalsize'])

    def test_stats_transient_file(self):
        from niprov.jsonfile import JsonFile
        repo = JsonFile(self.dependencies)
        repo.all = Mock()
        records = [{},{},{},{},{},{},{},{},{},{},{}]
        totalsize = 0
        for r in records:
            r['size'] = random.randint(1,1000)
            totalsize += r['size']
        totalsize -= records[3]['size']
        del records[3]['size']
        repo.all.return_value = [self.imageWithProvenance(r) for r in records]
        out = repo.statistics()
        self.assertEqual(totalsize, out['totalsize'])
        
    def test_byId(self):
        from niprov.jsonfile import JsonFile
        repo = JsonFile(self.dependencies)
        img1 = self.imageWithProvenance({'id':'1'})
        img2 = self.imageWithProvenance({'id':'2'})
        img3 = self.imageWithProvenance({'id':'3'})
        repo.all = Mock()
        repo.all.return_value = [img1, img2, img3]
        out = repo.byId('2')
        self.assertEqual(img2, out)

    def test_bySubject_doesnt_balk_if_no_subject_field(self):
        from niprov.jsonfile import JsonFile
        repo = JsonFile(self.dependencies)
        img1 = self.imageWithProvenance({'a':'b'})
        img2 = self.imageWithProvenance({'subject':'tim','a':'d'})
        img3 = self.imageWithProvenance({'subject':'john','a':'f'})
        repo.all = Mock()
        repo.all.return_value = [img1, img2, img3]
        out = repo.bySubject('john')

    def test_byLocations(self):
        self.fileFactory.fromProvenance.side_effect = lambda p: 'img_'+p['a']
        from niprov.jsonfile import JsonFile
        repo = JsonFile(self.dependencies)
        img1 = self.imageWithProvenance({'location':'i'})
        img2 = self.imageWithProvenance({'location':'j'})
        img3 = self.imageWithProvenance({'location':'m'})
        img4 = self.imageWithProvenance({'location':'f'})
        img5 = self.imageWithProvenance({'location':'x'})
        repo.all = Mock()
        repo.all.return_value = [img1,img2,img3,img4,img5]
        out = repo.byLocations(['j','f','k'])
        self.assertEqual([img2, img4], out)

    def test_byParents(self):
        self.fileFactory.fromProvenance.side_effect = lambda p: 'img_'+p['l']
        from niprov.jsonfile import JsonFile
        repo = JsonFile(self.dependencies)
        img1 = self.imageWithProvenance({'parents':[],'l':'a'})
        img2 = self.imageWithProvenance({'parents':['x','a'],'l':'b'})
        img3 = self.imageWithProvenance({'parents':['b'],'l':'b'})
        img4 = self.imageWithProvenance({'parents':['c','y'],'l':'d'})
        img5 = self.imageWithProvenance({'parents':['d'],'l':'e'})
        repo.all = Mock()
        repo.all.return_value = [img1, img2, img3, img4, img5]
        out = repo.byParents(['x','y'])
        self.assertEqual([img2, img4], out)

