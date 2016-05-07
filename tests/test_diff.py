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

    def test_areEqualProtocol_selects_on_BaseFile_getProtocolFields(self):
        from niprov.diff import Diff
        diff = Diff(self.fileWithP({'a':1,'x':7}, protocol=['x']), 
                    self.fileWithP({'a':2,'x':7}))
        self.assertTrue(diff.areEqualProtocol())
        diff = Diff(self.fileWithP({'a':1,'x':7}, protocol=['x']), 
                    self.fileWithP({'a':2,'x':8}))
        self.assertFalse(diff.areEqualProtocol())

    def test_assertEqualProtocol_throws_if_not_areEqualProtocol(self):
        from niprov.diff import Diff
        diff = Diff(self.fileWithP({'a':1,'x':7}, protocol=['x']), 
                    self.fileWithP({'a':2,'x':8}))
        with self.assertRaises(AssertionError):
            diff.assertEqualProtocol()

    def test_getDifferenceString(self):
        from niprov.diff import Diff
        n = Diff.NCHARSCOL
        diff = Diff(self.fileWithP({'a':1}), 
                    self.fileWithP({'a':2,'b':3}))
        diffStr = diff.getDifferenceString()
        line = ' '.ljust(n)+'afilename'.ljust(n)+' '+'afilename'.ljust(n)
        self.assertIn(line, diffStr)
        line = 'a'.ljust(n)+' '+str(1).ljust(n)+' '+str(2).ljust(n)
        self.assertIn(line, diffStr)
        line = 'b'.ljust(n)+' '+'n/a'.ljust(n)+' '+str(3).ljust(n)
        self.assertIn(line, diffStr)

    def test_assertEqual_exception_message_is_getDifferenceString(self):
        from niprov.diff import Diff
        n = Diff.NCHARSCOL
        diff = Diff(self.fileWithP({'a':1}), 
                    self.fileWithP({'a':2,'b':2}))
        exception = None
        try:
            diff.assertEqual()
        except AssertionError as e:
            exception = e
        self.assertIsNotNone(exception, 'No AssertionError raised')
        self.assertEqual(diff.getDifferenceString(), str(e))

    def test_Diff_to_string_is_(self):
        from niprov.diff import Diff
        diff = Diff(self.fileWithP({'a':1}), 
                    self.fileWithP({'a':2}))
        self.assertEqual(diff.getDifferenceString(), str(diff))

    def test_getSame(self):
        from niprov.diff import Diff
        diff = Diff(self.fileWithP({'a':1,'b':2}), 
                    self.fileWithP({'a':1,'b':3}))
        self.assertEqual(diff.getSame(), {'a':'same'})

    def test_getSameString(self):
        from niprov.diff import Diff
        n = Diff.NCHARSCOL
        diff = Diff(self.fileWithP({'a':1}), 
                    self.fileWithP({'a':1,'b':3}))
        diffStr = diff.getSameString()
        line = ' '.ljust(n)+'afilename'.ljust(n)+' '+'afilename'.ljust(n)
        self.assertIn(line, diffStr)
        line = 'a'.ljust(n)+' '+str(1).ljust(n)+' '+str(1).ljust(n)
        self.assertIn(line, diffStr)

    def fileWithP(self, provenance, protocol=None):
        mfile = Mock()
        mfile.location = 'afilename'
        mfile.getProvenance.return_value = provenance
        mfile.getProtocolFields.return_value = protocol
        return mfile



