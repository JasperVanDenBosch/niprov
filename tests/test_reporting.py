import unittest
from mock import Mock

class ReportingTests(unittest.TestCase):

    def setUp(self):
        self.factory = Mock()
        self.repo = Mock()
        self.listener = Mock()
        self.exporter = Mock()
        self.factory.createExporter.return_value = self.exporter

    def report(self, *args, **kwargs):
        import niprov
        return niprov.report(*args, repository=self.repo, exportFactory=self.factory,
            listener=self.listener, **kwargs)

    def test_Without_specifics_returns_all_files(self):
        out = self.report()
        self.exporter.export.assert_called_with(self.repo.all())
        self.assertEqual(out, self.exporter.export())

    def test_Can_report_on_one_file_specifically(self):
        out = self.report(forFile='afile.f')
        self.exporter.export.assert_called_with(self.repo.byPath('afile.f'))
        self.assertEqual(out, self.exporter.export())

    def test_Can_report_on_all_files_for_subject(self):
        out = self.report(forSubject='Jane Doe')
        self.exporter.export.assert_called_with(
            self.repo.bySubject('Jane Doe'))
        self.assertEqual(out, self.exporter.export())

    def test_Obtains_exporter_from_factory(self):
        import niprov
        factory = Mock()
        repo = Mock()
        niprov.report(repository=repo, exportFactory=factory)
        factory.createExporter.assert_any_call(None, None)
        niprov.report(medium='html', repository=repo, exportFactory=factory)
        factory.createExporter.assert_any_call('html', None)
        niprov.report(form='narrative', repository=repo, exportFactory=factory)
        factory.createExporter.assert_any_call(None, 'narrative')

    def test_Passes_provenance_to_exporter(self):
        import niprov
        factory = Mock()
        repo = Mock()
        niprov.report(repository=repo, exportFactory=factory)
        factory.createExporter().export.assert_any_call(repo.all())
        niprov.report(forSubject='Jane', repository=repo, exportFactory=factory)
        factory.createExporter().export.assert_any_call(repo.bySubject())

    def test_Passes_single_item_of_provenance_to_exporter(self):
        import niprov
        factory = Mock()
        repo = Mock()
        niprov.report(forFile='xyz',repository=repo, exportFactory=factory)
        factory.createExporter().export.assert_any_call(repo.byPath('xyz'))

    def test_If_file_unknown_tells_listener(self):
        self.repo.knowsByPath.return_value = False
        self.repo.byPath.side_effect = IndexError
        self.report(forFile='xyz')
        self.listener.unknownFile.assert_called_with('xyz')



