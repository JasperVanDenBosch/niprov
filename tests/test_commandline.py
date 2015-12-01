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

    def test_Only_prints_if_appropriate_verbosity_setting(self):
        from niprov.commandline import Commandline
        self.dependencies.config.verbosity = 'warning'
        with patch('__builtin__.print') as mprint:
            cmd = Commandline(self.dependencies)
            cmd.log('info','Do you remember..')
            assert not mprint.called
            cmd.log('warning','Watch out!')
            mprint.assert_called_with('[provenance:warning] Watch out!')

        
