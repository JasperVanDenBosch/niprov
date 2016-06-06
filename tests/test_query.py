from tests.ditest import DependencyInjectionTestBase
from mock import Mock, sentinel, patch


class QueryTest(DependencyInjectionTestBase):

    def setUp(self):
        super(QueryTest, self).setUp()

    def test_byModality(self):
        from niprov.querying import Query
        q = Query().byModality('magic')
        self.assertEqual(1, len(q.getFields()))
        self.assertEqual('modality', q.getFields()[0].name)
        self.assertEqual('magic', q.getFields()[0].value)

        
    

