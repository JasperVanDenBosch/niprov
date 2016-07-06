import unittest
from mock import Mock, patch
from tests.ditest import DependencyInjectionTestBase


class ContextTests(DependencyInjectionTestBase):

    def setUp(self):
        super(ContextTests, self).setUp()
        patcher = patch('niprov.context.niprov')
        self.niprov = patcher.start()
        self.addCleanup(patcher.stop)
        from niprov import ProvenanceContext
        self.context = ProvenanceContext()
        self.context.deps = self.dependencies

    def test_get(self):
        self.assertEqual(self.context.get(), self.query)

    def test_add(self):
        self.context.add('file.p', True, {'c':3})
        self.niprov.adding.add.assert_called_with('file.p', True, {'c':3},
            self.dependencies)



