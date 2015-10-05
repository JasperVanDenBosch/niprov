import unittest
from mock import Mock, patch, sentinel


class MongoRepoTests(unittest.TestCase):

    def setUp(self):
        self.dependencies = Mock()
        self.config = Mock()
        self.factory = Mock()
        self.dependencies.getConfiguration.return_value = self.config
        self.dependencies.getFileFactory.return_value = self.factory
        self.db = Mock()

    def setupRepo(self):
        from niprov.mongo import MongoRepository
        with patch('niprov.mongo.pymongo') as pymongo:
            self.repo = MongoRepository(dependencies=self.dependencies)
        self.repo.db = self.db

    def test_Connection(self):
        from niprov.mongo import MongoRepository
        with patch('niprov.mongo.pymongo') as pymongo:
            repo = MongoRepository(dependencies=self.dependencies)
        pymongo.MongoClient.assert_called_with(self.config.database_url)
        self.assertEqual(pymongo.MongoClient().get_default_database(), repo.db)

    def test_knowsByLocation(self):
        self.setupRepo()
        p = '/p/f1'
        self.db.provenance.find_one.return_value = None
        self.assertFalse(self.repo.knowsByLocation(p))
        self.db.provenance.find_one.assert_called_with({'location':p})
        self.db.provenance.find_one.return_value = 1
        self.assertTrue(self.repo.knowsByLocation(p))

    def test_byLocation_returns_img_from_record_with_path(self):
        self.setupRepo()
        p = '/p/f1'
        out = self.repo.byLocation(p)
        self.db.provenance.find_one.assert_called_with({'location':p})
        self.factory.fromProvenance.assert_called_with(
            self.db.provenance.find_one())
        self.assertEqual(self.factory.fromProvenance(), out)

    def test_getSeries(self):
        self.setupRepo()
        img = Mock()
        out = self.repo.getSeries(img)
        self.db.provenance.find_one.assert_called_with(
            {'seriesuid':img.getSeriesId()})
        self.factory.fromProvenance.assert_called_with(
            self.db.provenance.find_one())
        self.assertEqual(self.factory.fromProvenance(), out)

    def test_knowsSeries_returns_False_if_no_series_id(self):
        self.setupRepo()
        img = Mock()
        img.getSeriesId.return_value = None
        self.assertFalse(self.repo.knowsSeries(img))

    def test_knowsSeries(self):
        self.setupRepo()
        img = Mock()
        self.assertTrue(self.repo.knowsSeries(img))
        self.db.provenance.find_one.return_value = None
        self.assertFalse(self.repo.knowsSeries(img))

    def test_Add(self):
        self.setupRepo()
        img = Mock()
        self.repo.add(img)
        self.db.provenance.insert_one.assert_called_with(img.provenance)

    def test_update(self):
        self.setupRepo()
        img = Mock()
        self.repo.update(img)
        self.db.provenance.update.assert_called_with(
            {'location':img.location.toString()}, img.provenance)

    def test_all(self):
        self.factory.fromProvenance.side_effect = lambda p: 'img_'+p
        self.db.provenance.find.return_value = ['p1', 'p2']
        self.setupRepo()
        out = self.repo.all()
        self.db.provenance.find.assert_called_with()
        self.factory.fromProvenance.assert_any_call('p1')
        self.factory.fromProvenance.assert_any_call('p2')
        self.assertEqual(['img_p1', 'img_p2'], out)

    def test_bySubject(self):
        self.factory.fromProvenance.side_effect = lambda p: 'img_'+p
        self.db.provenance.find.return_value = ['p1', 'p2']
        self.setupRepo()
        s = 'Brambo'
        out = self.repo.bySubject(s)
        self.db.provenance.find.assert_called_with({'subject':s})
        self.factory.fromProvenance.assert_any_call('p1')
        self.factory.fromProvenance.assert_any_call('p2')
        self.assertEqual(['img_p1', 'img_p2'], out)

    def test_byApproval(self):
        self.factory.fromProvenance.side_effect = lambda p: 'img_'+p
        self.db.provenance.find.return_value = ['p1', 'p2']
        self.setupRepo()
        a = 'AOk'
        out = self.repo.byApproval(a)
        self.db.provenance.find.assert_called_with({'approval':a})
        self.factory.fromProvenance.assert_any_call('p1')
        self.factory.fromProvenance.assert_any_call('p2')
        self.assertEqual(['img_p1', 'img_p2'], out)

    def test_updateApproval(self):
        self.setupRepo()
        img = Mock()
        p = '/p/f1'
        newStatus = 'oh-oh'
        self.repo.updateApproval(p, newStatus)
        self.db.provenance.update.assert_called_with(
            {'location':p}, {'$set': {'approval': newStatus}})

    def test_latest(self):
        self.factory.fromProvenance.side_effect = lambda p: 'img_'+p
        self.db.provenance.find.return_value.sort.return_value.limit.return_value = ['px','py']
        self.setupRepo()
        out = self.repo.latest()
        self.db.provenance.find.assert_called_with()
        self.db.provenance.find().sort.assert_called_with('added', -1)
        self.db.provenance.find().sort().limit.assert_called_with(20)
        self.factory.fromProvenance.assert_any_call('px')
        self.factory.fromProvenance.assert_any_call('py')
        self.assertEqual(['img_px', 'img_py'], out)

    def test_statistics(self):
        self.db.provenance.aggregate.return_value = [sentinel.stats,]
        self.setupRepo()
        out = self.repo.statistics()
        self.db.provenance.aggregate.assert_called_with(
           [{'$group':
                 {
                   '_id': None,
                   'totalsize': { '$sum': '$size' },
                   'count': { '$sum': 1 }
                 }
            }])
        self.assertEqual(sentinel.stats, out)

    def test_statistics_if_no_records(self):
        self.db.provenance.aggregate.return_value = []
        self.setupRepo()
        out = self.repo.statistics()
        self.assertEqual({'count':0}, out)

    def test_byId(self):
        self.setupRepo()
        ID = 'abc123'
        out = self.repo.byId(ID)
        self.db.provenance.find_one.assert_called_with({'id':ID})
        self.factory.fromProvenance.assert_called_with(
            self.db.provenance.find_one())
        self.assertEqual(self.factory.fromProvenance(), out)


