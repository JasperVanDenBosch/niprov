import unittest, os
from mock import Mock, patch, call
from tests.ditest import DependencyInjectionTestBase


class DiffTests(DependencyInjectionTestBase):

    def setUp(self):
        super(DiffTests, self).setUp()

    def test_areEqual_true_for_same_provenance(self):
        from niprov.diff import Diff
        diff = Diff(self.fileWithP({'a':1,'b':2}), 
                    self.fileWithP({'a':1,'b':2}))
        self.assertTrue(diff.areEqual())

    def test_areEqual_false_for_missing_key(self):
        from niprov.diff import Diff
        diff = Diff(self.fileWithP({'a':1,'b':2,'c':3}), 
                    self.fileWithP({'a':1,'b':2}))
        self.assertFalse(diff.areEqual())
        diff = Diff(self.fileWithP({'a':1,'b':2}), 
                    self.fileWithP({'a':1,'b':2,'d':4}))
        self.assertFalse(diff.areEqual())

    def fileWithP(self, provenance):
        mfile = Mock()
        mfile.getProvenance.return_value = provenance
        return mfile



