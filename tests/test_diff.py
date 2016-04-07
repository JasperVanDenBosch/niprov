import unittest, os
from mock import Mock, patch, call
from tests.ditest import DependencyInjectionTestBase


class DiffTests(DependencyInjectionTestBase):

    def setUp(self):
        super(DiffTests, self).setUp()

    def test_areEqual_true_for_same_provenance(self):
        from niprov.diff import Diff
        file1 = self.baseFileMock({'a':1,'b':2})
        file2 = self.baseFileMock({'a':1,'b':2})
        diff = Diff(file1, file2)
        self.assertTrue(diff.areEqual())

    def baseFileMock(self, provenance):
        mfile = Mock()
        mfile.getProvenance.return_value = provenance
        return mfile


