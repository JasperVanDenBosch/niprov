import unittest, os
from mock import Mock, patch, call
from tests.ditest import DependencyInjectionTestBase


class DiffTests(DependencyInjectionTestBase):

    def setUp(self):
        super(DiffTests, self).setUp()

    def test_assertSame(self):
        # method on Diff object that throws an AssertionError if
        # provenance is different
        pass

    def test_assertSame_with_fieldsOfInterest(self):
        # only raises AssertionError if passed keys are different
        # or don't exist in either object
        pass


