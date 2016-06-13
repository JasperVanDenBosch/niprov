import unittest
from mock import Mock
from tests.ditest import DependencyInjectionTestBase


class ContextTests(DependencyInjectionTestBase):

    def setUp(self):
        super(ContextTests, self).setUp()
        from niprov import Context
        self.context = Context()
        self.context.deps = self.dependencies

    def test_get(self):
        self.assertEqual(self.context.get(), self.query)



