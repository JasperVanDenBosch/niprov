import unittest
from mock import Mock

class ReportingTests(unittest.TestCase):

    def test_Without_specifics_returns_all_files(self):
        import niprov
        log = Mock()
        repo = Mock()
        out = niprov.report(repository=repo, exportFactory=Mock())
        self.assertEqual(out, repo.all())

    def test_Can_report_on_one_file_specifically(self):
        import niprov
        log = Mock()
        repo = Mock()
        repo.byPath.side_effect = lambda x: ('prov for', x)
        out = niprov.report(forFile='afile.f', repository=repo, 
            exportFactory=Mock())
        self.assertEqual(out, repo.byPath('afile.f'))

    def test_Can_report_on_all_files_for_subject(self):
        import niprov
        log = Mock()
        repo = Mock()
        repo.bySubject.side_effect = lambda x: ('prov for', x)
        out = niprov.report(forSubject='Jane Doe', repository=repo, 
            exportFactory=Mock())
        self.assertEqual(out, repo.bySubject('Jane Doe'))

    def test_Obtains_exporter_from_factory_and_passes_it_provenance(self):
        import niprov
        factory = Mock()
        repo = Mock()
        niprov.report(repository=repo, exportFactory=factory)
        factory.createExporter.assert_any_call(None)
        niprov.report(format='html', repository=repo, exportFactory=factory)
        factory.createExporter.assert_any_call('html')

    def test_Passes_provenance_to_exporter(self):
        import niprov
        factory = Mock()
        repo = Mock()
        niprov.report(repository=repo, exportFactory=factory)
        factory.createExporter().exportList.assert_any_call(repo.all())



