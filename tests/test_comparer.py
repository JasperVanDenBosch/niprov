import unittest, os
from mock import Mock, patch, sentinel
from tests.ditest import DependencyInjectionTestBase


class ComparerTests(DependencyInjectionTestBase):

    def setUp(self):
        super(ComparerTests, self).setUp()

    def test_compare_returns_Diff_object(self):
        from niprov.comparing import compare
        from niprov.diff import Diff
        out = compare(self.mockFile(), self.mockFile(), self.dependencies)
        self.assertIsInstance(out, Diff)

    def test_compare_creates_basic_diff(self):
        from niprov.comparing import compare
        with patch('niprov.comparing.Diff') as DiffCtor:
            compare(sentinel.f1, sentinel.f2, self.dependencies)
            DiffCtor.assert_called_with(sentinel.f1, sentinel.f2)

    def mockFile(self):
        f = Mock()
        f.getProvenance.return_value = {}
        return f

