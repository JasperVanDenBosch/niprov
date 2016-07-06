import unittest
from mock import Mock, patch
from tests.ditest import DependencyInjectionTestBase


class ContextTests(DependencyInjectionTestBase):

    def setUp(self):
        super(ContextTests, self).setUp()
        patcher = patch('niprov.context.niprov')
        self.niprov = patcher.start()
        self.addCleanup(patcher.stop)
        from niprov import ProvenanceContext
        self.context = ProvenanceContext()
        self.context.deps = self.dependencies

    def test_get(self):
        self.assertEqual(self.context.get(), self.query)

    def test_add(self):
        self.context.add('file.p', True, {'c':3})
        self.niprov.adding.add.assert_called_with('file.p', True, {'c':3},
            self.dependencies)

    def test_log(self):
        self.context.log('new', 'trf', 'parents', 'code', 'logtext', False,
            'script', 'user', {'prov':1}, 'opts')
        self.niprov.logging.log.assert_called_with('new', 'trf', 'parents', 
            'code', 'logtext', False, 'script', 'user', {'prov':1}, 'opts',
            self.dependencies)

    def test_backup(self):
        self.context.backup()
        self.niprov.exporting.backup.assert_called_with(self.dependencies)

    def test_export(self):
        self.context.export('prov', 'medium', 'form')
        self.niprov.exporting.export.assert_called_with('prov', 'medium',
            'form', False, self.dependencies)

    def test_import(self):
        self.context.importp('fpath')
        self.niprov.importing.importp.assert_called_with('fpath',
            self.dependencies)

    def test_print(self):
        self.context.print_('images')
        self.niprov.exporting.print_.assert_called_with('images', False, 
            self.dependencies)

    def test_record(self):
        self.context.record('cmd', 'new', 'parents', True, 'args', 'kwargs', 
            'user', 'opts')
        self.niprov.recording.record.assert_called_with('cmd', 'new', 
            'parents', True, 'args', 'kwargs', 'user', 'opts',
            self.dependencies)

    def test_view(self):
        self.context.view('images', pipeline=True)
        self.niprov.exporting.view.assert_called_with('images', True, 
            self.dependencies)



