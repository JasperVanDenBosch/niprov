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

    def test_bySubject(self):
        from niprov.querying import Query
        q = Query(self.dependencies).bySubject('potter, h')
        self.assertEqual(1, len(q.getFields()))
        self.assertEqual('subject', q.getFields()[0].name)
        self.assertEqual('potter, h', q.getFields()[0].value)

    def test_byApproval(self):
        from niprov.querying import Query
        q = Query(self.dependencies).byApproval('ceterum censeo')
        self.assertEqual(1, len(q.getFields()))
        self.assertEqual('approval', q.getFields()[0].name)
        self.assertEqual('ceterum censeo', q.getFields()[0].value)

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

    def test_In_on_query(self):
        from niprov.querying import Query
        self.repo.inquire.return_value = [sentinel.r1, sentinel.r2]
        q = Query(self.dependencies).bySubject('abc')
        self.assertTrue(sentinel.r2 in q)

    def test_Len_or_Iter_or_in_only_runs_inquire_once(self):
        from niprov.querying import Query
        self.repo.inquire.return_value = [sentinel.r1, sentinel.r2]
        q = Query(self.dependencies)
        len(q)
        list(q)
        sentinel.r2 in q
        self.assertEqual(self.repo.inquire.call_count, 1)

    def test_byLocation(self):
        self.locationFactory.completeString.side_effect = lambda s: s
        from niprov.querying import Query
        result = Query(self.dependencies).byLocation('abc')
        self.repo.byLocation.assert_called_with('abc')
        self.assertEqual(result, self.repo.byLocation('abc'))

    def test_Statistics(self):
        from niprov.querying import Query
        result = Query(self.dependencies).statistics()
        self.repo.statistics.assert_called_with()
        self.assertEqual(result, self.repo.statistics())

    def test_Latest(self):
        from niprov.querying import Query
        result = Query(self.dependencies).latest()
        self.repo.latest.assert_called_with()
        self.assertEqual(result, self.repo.latest())

    def test_All(self):
        from niprov.querying import Query
        result = Query(self.dependencies).all()
        self.repo.all.assert_called_with()
        self.assertEqual(result, self.repo.all())

    def test_Completes_locationString_byLocation(self):
        from niprov.querying import Query
        result = Query(self.dependencies).byLocation('abc')
        self.locationFactory.completeString.assert_any_call('abc')
        self.repo.byLocation.assert_called_with(self.locationFactory.completeString())

    def test_allModalities(self):
        from niprov.querying import Query
        q = Query(self.dependencies).allModalities()
        self.assertEqual('modality', q.getFields()[0].name)
        self.assertTrue(q.getFields()[0].all)

    def test_allUsers(self):
        from niprov.querying import Query
        q = Query(self.dependencies).allUsers()
        self.assertEqual('user', q.getFields()[0].name)
        self.assertTrue(q.getFields()[0].all)

    def test_allProjects(self):
        from niprov.querying import Query
        q = Query(self.dependencies).allProjects()
        self.assertEqual('project', q.getFields()[0].name)
        self.assertTrue(q.getFields()[0].all)

    def test_copiesOf_returns_empty_list_for_size_0_file(self):
        from niprov.querying import Query
        target = Mock()
        target.provenance = {'size':0}
        results = Query(self.dependencies).copiesOf(target)
        self.assertEqual(0, len(results))

    def test_copiesOf(self):
        from niprov.querying import Query
        target = Mock()
        target.provenance = {'hash':'a7b8c9', 'size':1}
        q = Query(self.dependencies).copiesOf(target)
        self.assertEqual(1, len(q.getFields()))
        self.assertEqual('hash', q.getFields()[0].name)
        self.assertEqual('a7b8c9', q.getFields()[0].value)



