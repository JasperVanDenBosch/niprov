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

    def test_byProject(self):
        from niprov.querying import Query
        q = Query().byProject('sealion')
        self.assertEqual(1, len(q.getFields()))
        self.assertEqual('project', q.getFields()[0].name)
        self.assertEqual('sealion', q.getFields()[0].value)

    def test_byUser(self):
        from niprov.querying import Query
        q = Query().byUser('dumbledore')
        self.assertEqual(1, len(q.getFields()))
        self.assertEqual('user', q.getFields()[0].name)
        self.assertEqual('dumbledore', q.getFields()[0].value)


