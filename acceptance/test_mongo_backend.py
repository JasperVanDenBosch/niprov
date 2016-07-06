import unittest, os
from pymongo import MongoClient

URL = 'mongodb://niprov-admin:{0}@ds041571.mongolab.com:41571/niprov'
PASSWORD = 'uU0mpDXtQXeL6wku'


class MongoTests(unittest.TestCase):

    def setUp(self):
        from niprov import ProvenanceContext
        self.provenance = ProvenanceContext()
        self.fullURL = URL.format(PASSWORD)
        self.provenance.config.database_type = 'MongoDB'
        self.provenance.config.database_url = self.fullURL

    def tearDown(self):
        client = MongoClient(self.fullURL)
        client.get_default_database().provenance.drop()

    @unittest.skipIf("TRAVIS" in os.environ, "Skipping this test on Travis CI.")
    def test_Something(self):
        self.provenance.discover('testdata')
        testfpath = os.path.abspath('testdata/parrec/T1.PAR')
        img = self.provenance.get().byLocation(testfpath)
        self.assertEqual(img.provenance['subject'], '05aug14test')

    @unittest.skipIf("TRAVIS" in os.environ, "Skipping this test on Travis CI.")
    def test_Stats(self):
        self.provenance.discover('testdata')
        repository = self.provenance.deps.getRepository()
        print(repository.statistics())



