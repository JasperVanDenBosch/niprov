import unittest, os
from mock import Mock, patch, call
from tests.ditest import DependencyInjectionTestBase


class CommandlineTests(DependencyInjectionTestBase):

    def setUp(self):
        super(CommandlineTests, self).setUp()

    def test_raises_exception_for_unknown_file(self):
        from niprov.commandline import Commandline
        from niprov.exceptions import UnknownFileError
        cmd = Commandline()
        with self.assertRaisesRegexp(UnknownFileError, '.* /foo/bar.baz'):
            cmd.unknownFile('/foo/bar.baz')
