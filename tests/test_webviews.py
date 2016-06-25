import unittest
from mock import Mock, patch
from tests.ditest import DependencyInjectionTestBase


class ViewTests(DependencyInjectionTestBase):

    def setUp(self):
        super(ViewTests, self).setUp()
        self.config.dryrun = False
        self.img = Mock()
        self.request = Mock()
        self.request.dependencies = self.dependencies

    def test_latest(self):
        import niprov.views
        out = niprov.views.latest(self.request)
        self.assertEqual(self.repo.latest(), out['images'])

    def test_by_id(self):
        import niprov.views
        self.request.matchdict = {'id':'1a2b3c'}
        out = niprov.views.short(self.request)
        self.repo.byId.assert_called_with('1a2b3c')
        self.assertEqual(self.repo.byId(), out['image'])

    def test_by_full_location(self):
        import niprov.views
        self.request.matchdict = {'host':'her','path':('a','b','c')}
        out = niprov.views.location(self.request)
        self.repo.byLocation.assert_called_with('her:/a/b/c')
        self.assertEqual(self.repo.byLocation(), out['image'])

    def test_stats(self):
        import niprov.views
        out = niprov.views.stats(self.request)
        self.assertEqual(self.repo.statistics(), out['stats'])

    def test_pipeline_by_id(self):
        import niprov.views
        self.request.matchdict = {'id':'1a2b3c'}
        out = niprov.views.pipeline(self.request)
        self.repo.byId.assert_called_with('1a2b3c')
        self.pipelineFactory.forFile.assert_called_with(self.repo.byId())
        self.assertEqual(self.pipelineFactory.forFile(), out['pipeline'])
        self.assertEqual(out['sid'], '1a2b3c')

    def test_by_project(self):
        import niprov.views
        self.request.matchdict = {'project':'failcow'}
        out = niprov.views.project(self.request)
        self.query.byProject.assert_called_with('failcow')
        self.assertEqual(self.query.byProject(), out['images'])

    def test_by_user(self):
        import niprov.views
        self.request.matchdict = {'user':'failcow'}
        out = niprov.views.user(self.request)
        self.query.byUser.assert_called_with('failcow')
        self.assertEqual(self.query.byUser(), out['images'])

    def test_by_modality(self):
        import niprov.views
        self.request.matchdict = {'modality':'failcow'}
        out = niprov.views.modality(self.request)
        self.query.byModality.assert_called_with('failcow')
        self.assertEqual(self.query.byModality(), out['images'])

    def test_by_subject(self):
        import niprov.views
        self.request.matchdict = {'subject':'janedoe'}
        out = niprov.views.subject(self.request)
        self.query.bySubject.assert_called_with('janedoe')
        self.assertEqual(self.query.bySubject(), out['images'])

    def test_search_provides_searchstring_to_template(self):
        import niprov.views
        self.request.GET = {'text':'hello world'}
        out = niprov.views.search(self.request)
        self.assertEqual('hello world', out['searchtext'])

    def test_search_provides_search_results_to_template(self):
        import niprov.views
        self.request.GET = {'text':'hello world'}
        with patch('niprov.views.searching') as searching:
            out = niprov.views.search(self.request)
            searching.search.assert_called_with('hello world',
                                                self.request.dependencies)
            self.assertEqual(searching.search(), out['images'])





