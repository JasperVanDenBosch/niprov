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

    def test_by_subject(self):
        import niprov.views
        self.request.matchdict = {'subject':'janedoe'}
        out = niprov.views.subject(self.request)
        self.repo.bySubject.assert_called_with('janedoe')
        self.assertEqual(self.repo.bySubject(), out['images'])





