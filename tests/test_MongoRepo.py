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

