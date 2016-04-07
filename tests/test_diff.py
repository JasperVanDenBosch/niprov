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

    def test_areEqual_false_for_different_value(self):
        from niprov.diff import Diff
        diff = Diff(self.fileWithP({'a':1}), 
                    self.fileWithP({'a':2}))
        self.assertFalse(diff.areEqual())

    def test_can_ignore_key(self):
        from niprov.diff import Diff
        diff = Diff(self.fileWithP({'a':1}), 
                    self.fileWithP({'a':1,'b':3}))
        self.assertTrue(diff.areEqual(ignore=['b','c']))
        diff = Diff(self.fileWithP({'a':1,'b':3}), 
                    self.fileWithP({'a':2,'b':3}))
        self.assertTrue(diff.areEqual(ignore=['a','c']))

    def test_areEqual_ignores_id_by_default(self):
        from niprov.diff import Diff
        diff = Diff(self.fileWithP({'_id':1,'b':3}), 
                    self.fileWithP({'_id':2,'b':3}))
        self.assertTrue(diff.areEqual())
        diff = Diff(self.fileWithP({'_id':1,'b':3}), 
                    self.fileWithP({'b':3}))
        self.assertTrue(diff.areEqual())
        diff = Diff(self.fileWithP({'_id':1,'b':3}), 
                    self.fileWithP({'b':3}))
        self.assertTrue(diff.areEqual(ignore=['d']))

    def test_can_select_specific_keys_and_ignore_the_rest(self):
        from niprov.diff import Diff
        diff = Diff(self.fileWithP({'a':1,'b':2,'c':3}), 
                    self.fileWithP({'a':1,'b':9,'c':3,'d':4}))
        self.assertTrue(diff.areEqual(select=['a','c']))
        self.assertFalse(diff.areEqual(select=['b']))
        self.assertFalse(diff.areEqual(select=['d']))

    def test_assertEqual_throws_for_different_value(self):
        from niprov.diff import Diff
        diff = Diff(self.fileWithP({'a':1}), 
                    self.fileWithP({'a':2}))
        with self.assertRaises(AssertionError):
            diff.assertEqual()

    def test_areEqualProtocol(self):
        from niprov.diff import Diff
        diff = Diff(self.fileWithP({'a':1,'x':7}, protocol=['x']), 
                    self.fileWithP({'a':2,'x':7}))
        self.assertTrue(diff.areEqualProtocol())
        diff = Diff(self.fileWithP({'a':1,'x':7}, protocol=['x']), 
                    self.fileWithP({'a':2,'x':8}))
        self.assertFalse(diff.areEqualProtocol())

    def fileWithP(self, provenance, protocol=None):
        mfile = Mock()
        mfile.getProvenance.return_value = provenance
        mfile.getProtocolFields.return_value = protocol
        return mfile



