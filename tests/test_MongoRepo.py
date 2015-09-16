import unittest
from mock import Mock, patch


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

    def test_knowsByPath(self):
        self.setupRepo()
        p = '/p/f1'
        self.db.provenance.find_one.return_value = None
        self.assertFalse(self.repo.knowsByPath(p))
        self.db.provenance.find_one.assert_called_with({'path':p})
        self.db.provenance.find_one.return_value = 1
        self.assertTrue(self.repo.knowsByPath(p))

    def test_byPath_returns_img_from_record_with_path(self):
        self.setupRepo()
        p = '/p/f1'
        out = self.repo.byPath(p)
        self.db.provenance.find_one.assert_called_with({'path':p})
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
        prov = Mock()
        self.repo.add(prov)
        self.db.provenance.insert_one.assert_called_with(prov)

    def test_update(self):
        self.setupRepo()
        img = Mock()
        self.repo.update(img)
        self.db.provenance.update.assert_called_with(
            {'path':img.path}, img.provenance)

    def test_all(self):
        self.factory.fromProvenance.side_effect = lambda p: 'img_'+p
        self.db.provenance.find.return_value = ['p1', 'p2']
        self.setupRepo()
        out = self.repo.all()
        self.db.provenance.find.assert_called_with()
        self.assertEqual(['p1', 'p2'], out)
#        self.factory.fromProvenance.assert_any_call('p1')
#        self.factory.fromProvenance.assert_any_call('p2')
#        self.assertEqual(['img_p1', 'img_p2'], out)

    def test_bySubject(self):
        self.factory.fromProvenance.side_effect = lambda p: 'img_'+p
        self.db.provenance.find.return_value = ['p1', 'p2']
        self.setupRepo()
        s = 'Brambo'
        out = self.repo.bySubject(s)
        self.db.provenance.find.assert_called_with({'subject':s})
        self.assertEqual(['p1', 'p2'], out)
#        self.factory.fromProvenance.assert_any_call('p1')
#        self.factory.fromProvenance.assert_any_call('p2')
#        self.assertEqual(['img_p1', 'img_p2'], out)

    def test_byApproval(self):
        self.factory.fromProvenance.side_effect = lambda p: 'img_'+p
        self.db.provenance.find.return_value = ['p1', 'p2']
        self.setupRepo()
        a = 'AOk'
        out = self.repo.byApproval(a)
        self.db.provenance.find.assert_called_with({'approval':a})
        self.assertEqual(['p1', 'p2'], out)

    def test_updateApproval(self):
        self.setupRepo()
        img = Mock()
        p = '/p/f1'
        newStatus = 'oh-oh'
        self.repo.updateApproval(p, newStatus)
        self.db.provenance.update.assert_called_with(
            {'path':p}, {'$set': {'approval': newStatus}})

