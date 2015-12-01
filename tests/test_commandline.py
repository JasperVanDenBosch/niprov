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

    def test_If_on_dryrun_mode_an_unknown_file_is_not_an_error(self):
        from niprov.commandline import Commandline
        from niprov.exceptions import UnknownFileError
        self.dependencies.config.verbosity = 'warning' #default
        self.dependencies.config.dryrun = False
        cmd = Commandline(self.dependencies)
        cmd.log = Mock()
        cmd.unknownFile('abc')
        cmd.log.assert_called_with('error','Unknown file: abc', UnknownFileError)
        self.dependencies.config.dryrun = True
        cmd = Commandline(self.dependencies)
        cmd.log = Mock()
        cmd.unknownFile('abc')
        cmd.log.assert_called_with('info','Unknown file: abc', UnknownFileError)


        
