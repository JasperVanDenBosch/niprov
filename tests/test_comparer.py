import unittest, os
from mock import Mock, patch, call
from tests.ditest import DependencyInjectionTestBase


class ComparerTests(DependencyInjectionTestBase):

    def setUp(self):
        super(ComparerTests, self).setUp()

    def test_compare_returns_Diff_object(self):
        from niprov.comparing import compare
        from niprov.diff import Diff
        out = compare(None, None, self.dependencies)
        self.assertIsInstance(out, Diff)
