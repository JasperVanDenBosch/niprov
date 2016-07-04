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

    def test_byLocation(self):
        from niprov.jsonfile import JsonFile
        repo = JsonFile(self.dependencies)
        img1 = self.imageWithProvenance({'location':'1','path':'a'})
        img2 = self.imageWithProvenance({'location':'2','path':'b'})
        repo.all = Mock()
        repo.all.return_value = [img1, img2]
        out = repo.byLocation('2')
        self.assertEqual(img2, out)

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

    def test_Will_tell_PictureCache_to_persist_known_Snapshot(self):
        from niprov.jsonfile import JsonFile
        repo = JsonFile(self.dependencies)
        img = self.imageWithProvenance({'location':'1','foo':'baz'})
        repo.add(img)
        self.pictureCache.saveToDisk.assert_called_with(for_=img)

    def test_Query_with_value_field(self):
        self.fileFactory.fromProvenance.side_effect = lambda p: 'img_'+p['l']
        from niprov.jsonfile import JsonFile
        repo = JsonFile(self.dependencies)
        img1 = self.imageWithProvenance({'a':'b'})
        img2 = self.imageWithProvenance({'color':'red','a':'d'})
        img3 = self.imageWithProvenance({'color':'blue','a':'f'})
        img4 = self.imageWithProvenance({'color':'red','a':'d'})
        repo.all = Mock()
        repo.all.return_value = [img1, img2, img3, img4]
        q = Mock()
        field1 = Mock()
        field1.name = 'color'
        field1.value = 'red'
        field1.all = False
        q.getFields.return_value = [field1]
        out = repo.inquire(q)
        self.assertEqual([img2, img4], out)

    def test_Search_only_returns_objects_which_have_needle(self):
        self.fileFactory.fromProvenance.side_effect = lambda p: 'img_'+p['l']
        from niprov.jsonfile import JsonFile
        repo = JsonFile(self.dependencies)
        img1 = self.imageWithProvenance({'transformation':'green blue'})
        img2 = self.imageWithProvenance({'transformation':'yellow red'})
        repo.all = Mock()
        repo.all.return_value = [img1, img2]
        out = repo.search('red')
        self.assertEqual([img2], out)

    def test_Search_sorts_results_by_number_of_matches(self):
        self.fileFactory.fromProvenance.side_effect = lambda p: 'img_'+p['l']
        from niprov.jsonfile import JsonFile
        repo = JsonFile(self.dependencies)
        img1 = self.imageWithProvenance({'transformation':'red bluered'})
        img2 = self.imageWithProvenance({'transformation':'red and green'})
        img3 = self.imageWithProvenance({'transformation':'red pruple red red'})
        img4 = self.imageWithProvenance({'transformation':'nuthin'})
        repo.all = Mock()
        repo.all.return_value = [img1, img2, img3, img4]
        out = repo.search('red')
        self.assertEqual([img3, img1, img2], out)

    def test_Search_looks_through_multiple_fields(self):
        self.fileFactory.fromProvenance.side_effect = lambda p: 'img_'+p['l']
        from niprov.jsonfile import JsonFile
        repo = JsonFile(self.dependencies)
        i1 = self.imageWithProvenance({'color':'red'})
        i2 = self.imageWithProvenance({'location':'redis'})
        i3 = self.imageWithProvenance({'user':'reddit'})
        i4 = self.imageWithProvenance({'subject':'red bastard'})
        i5 = self.imageWithProvenance({'protocol':'reddish'})
        i6 = self.imageWithProvenance({'transformation':'zoomed red'})
        i7 = self.imageWithProvenance({'technique':'redshift'})
        i8 = self.imageWithProvenance({'modality':'red'})
        repo.all = Mock()
        repo.all.return_value = [i1,i2,i3,i4,i5,i6,i7,i8]
        out = repo.search('red')
        self.assertNotIn(i1, out)
        self.assertIn(i2, out)
        self.assertIn(i3, out)
        self.assertIn(i4, out)
        self.assertIn(i5, out)
        self.assertIn(i6, out)
        self.assertIn(i7, out)
        self.assertIn(i8, out)

    def test_Search_distinguishes_words_as_OR_search(self):
        self.fileFactory.fromProvenance.side_effect = lambda p: 'img_'+p['l']
        from niprov.jsonfile import JsonFile
        repo = JsonFile(self.dependencies)
        i1 = self.imageWithProvenance({'transformation':'blue red red'})       #2
        i2 = self.imageWithProvenance({'transformation':'red blue green red'}) #3
        i3 = self.imageWithProvenance({'transformation':'green blue'})         #1
        repo.all = Mock()
        repo.all.return_value = [i1,i2,i3]
        out = repo.search('red green')
        self.assertEqual([i2, i1, i3], out)

    def test_Search_returns_max_20_results(self):
        self.fileFactory.fromProvenance.side_effect = lambda p: 'img_'+p['l']
        from niprov.jsonfile import JsonFile
        repo = JsonFile(self.dependencies)
        recs = []
        for i in range(35):
            recs.append(self.imageWithProvenance({'transformation':'red'}))
        repo.all = Mock()
        repo.all.return_value = recs
        out = repo.search('red')
        self.assertEqual(20, len(out))

    def test_Query_with_ALL_field(self):
        self.fileFactory.fromProvenance.side_effect = lambda p: 'img_'+p['l']
        from niprov.jsonfile import JsonFile
        repo = JsonFile(self.dependencies)
        img1 = self.imageWithProvenance({'a':'b'})
        img2 = self.imageWithProvenance({'color':'red','a':'d'})
        img3 = self.imageWithProvenance({'color':'blue','a':'f'})
        img4 = self.imageWithProvenance({'color':'green','a':'d'})
        img5 = self.imageWithProvenance({'color':'blue','a':'g'})
        repo.all = Mock()
        repo.all.return_value = [img1, img2, img3, img4, img5]
        q = Mock()
        field1 = Mock()
        field1.name = 'color'
        field1.all = True
        q.getFields.return_value = [field1]
        out = repo.inquire(q)
        self.assertIn('red', out)
        self.assertIn('green', out)
        self.assertIn('blue', out)
        self.assertEqual(3, len(out))

    def test_getSeries(self):
        from niprov.jsonfile import JsonFile
        repo = JsonFile(self.dependencies)
        img = Mock()
        img.getSeriesId.return_value = '2'
        img1 = self.imageWithProvenance({'seriesuid':'1','path':'a'})
        img2 = self.imageWithProvenance({'seriesuid':'2','path':'b'})
        repo.all = Mock()
        repo.all.return_value = [img1, img2]
        out = repo.getSeries(img)
        self.assertEqual(img2, out)

    def test_getSeries_returns_None_right_away_if_no_series_id(self):
        from niprov.jsonfile import JsonFile
        repo = JsonFile(self.dependencies)
        img = Mock()
        img.getSeriesId.return_value = None
        repo.all = Mock()
        out = repo.getSeries(img)
        assert not repo.all.called, "Should not be called if no series id"
        self.assertEqual(None, out)

