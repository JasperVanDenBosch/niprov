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





