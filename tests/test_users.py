import unittest
from mock import Mock, patch, call
import os
from tests.ditest import DependencyInjectionTestBase


class UsersTests(DependencyInjectionTestBase):

    def setUp(self):
        super(UsersTests, self).setUp()

    def test_determineUser_if_not_config_or_runtime_uses_OS(self):
        from niprov.users import determineUser
        import getpass
        self.assertEqual(determineUser(), getpass.getuser())

