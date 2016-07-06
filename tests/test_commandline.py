import unittest, os
from mock import Mock, patch, call
from tests.ditest import DependencyInjectionTestBase


class CommandlineTests(DependencyInjectionTestBase):

    def setUp(self):
        super(CommandlineTests, self).setUp()

    def test_Only_prints_if_appropriate_verbosity_setting(self):
        from niprov.commandline import Commandline
        self.dependencies.config.verbosity = 'warning'
        with patch('__builtin__.print') as mprint:
            cmd = Commandline(self.dependencies)
            cmd.log('info','Do you remember..')
            assert not mprint.called
            cmd.log('warning','Watch out!')
            mprint.assert_called_with('[provenance:warning] Watch out!')

    def test_exportedToFile_logs_info(self):
        from niprov.commandline import Commandline
        self.dependencies.config.verbosity = 'info'
        cmd = Commandline(self.dependencies)
        cmd.log = Mock()
        cmd.exportedToFile('backupfile.x')
        cmd.log.assert_called_with('info','Exported to file: backupfile.x')

    def test_addUnknownParent(self):
        from niprov.commandline import Commandline
        self.dependencies.config.verbosity = 'info'
        cmd = Commandline(self.dependencies)
        cmd.log = Mock()
        cmd.addUnknownParent('backupfile.x')
        cmd.log.assert_called_with('warning', 'backupfile.x unknown. Adding to provenance')

    def test_fileAdded(self):
        from niprov.commandline import Commandline
        self.dependencies.config.verbosity = 'info'
        cmd = Commandline(self.dependencies)
        cmd.log = Mock()
        img = Mock()
        img.path = 'xyz'
        img.status = 'new'
        cmd.fileAdded(img)
        cmd.log.assert_called_with('info', 'New file: xyz')
        img.status = 'series-new-file'
        img.provenance = {'filesInSeries':[1, 2, 3]}
        img.getSeriesId.return_value = 'series987'
        cmd.fileAdded(img)
        cmd.log.assert_called_with('info', 'Added 3rd file to series: series987')
        img.status = 'new-version'
        cmd.fileAdded(img)
        cmd.log.assert_called_with('info', 'Added new version for: xyz')

    def test_usingCopyAsParent(self):
        from niprov.commandline import Commandline
        self.dependencies.config.verbosity = 'info'
        cmd = Commandline(self.dependencies)
        cmd.log = Mock()
        copy = Mock()
        copy.location = 'moon:/copy/location'
        cmd.usingCopyAsParent(copy)
        cmd.log.assert_called_with('warning', 
            'Used provenance from copy found at '+str(copy.location))
        

