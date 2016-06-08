from tests.ditest import DependencyInjectionTestBase
from mock import Mock, sentinel, patch


class QueryTest(DependencyInjectionTestBase):

    def setUp(self):
        super(QueryTest, self).setUp()

    def test_byModality(self):
        from niprov.querying import Query
        q = Query(self.dependencies).byModality('magic')
        self.assertEqual(1, len(q.getFields()))
        self.assertEqual('modality', q.getFields()[0].name)
        self.assertEqual('magic', q.getFields()[0].value)

    def test_byProject(self):
        from niprov.querying import Query
        q = Query(self.dependencies).byProject('sealion')
        self.assertEqual(1, len(q.getFields()))
        self.assertEqual('project', q.getFields()[0].name)
        self.assertEqual('sealion', q.getFields()[0].value)

    def test_byUser(self):
        from niprov.querying import Query
        q = Query(self.dependencies).byUser('dumbledore')
        self.assertEqual(1, len(q.getFields()))
        self.assertEqual('user', q.getFields()[0].name)
        self.assertEqual('dumbledore', q.getFields()[0].value)

    def test_Iter_returns_repository_inquire_results(self):
        from niprov.querying import Query
        self.repo.inquire.return_value = [sentinel.r1, sentinel.r2]
        q = Query(self.dependencies)
        out = list(q)
        self.repo.inquire.assert_called_with(q)
        self.assertEqual(out, self.repo.inquire())

    def test_Len_on_query(self):
        from niprov.querying import Query
        self.repo.inquire.return_value = [sentinel.r1, sentinel.r2]
        q = Query(self.dependencies)
        self.assertEqual(len(q), 2)


