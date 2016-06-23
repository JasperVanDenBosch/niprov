import unittest
from mock import Mock
from tests.ditest import DependencyInjectionTestBase


class SearchTests(DependencyInjectionTestBase):

    def setUp(self):
        super(SearchTests, self).setUp()

    def test_Search_delegates_to_repository(self):
        from niprov.searching import search
        results = search('one day', dependencies=self.dependencies)
        self.repo.search.assert_called_with('one day')
        self.assertEqual(results, self.repo.search())

