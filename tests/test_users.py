import unittest
from mock import Mock, patch, call
import os
from tests.ditest import DependencyInjectionTestBase


class UsersTests(DependencyInjectionTestBase):

    def setUp(self):
        super(UsersTests, self).setUp()
        self.config.user = None

    def test_determineUser_if_not_config_or_runtime_uses_OS(self):
        from niprov.users import Users
        users = Users(self.dependencies)
        import getpass
        self.assertEqual(users.determineUser(None), getpass.getuser())

    def test_determineUser_if_not_runtime_uses_config(self):
        from niprov.users import Users
        users = Users(self.dependencies)
        self.config.user = 'jasmine'
        self.assertEqual(users.determineUser(None), 'jasmine')

    def test_determineUser_if_runtime_given_uses_that(self):
        from niprov.users import Users
        users = Users(self.dependencies)
        self.config.user = 'jasmine'
        self.assertEqual(users.determineUser('oddyseus'), 'oddyseus')

