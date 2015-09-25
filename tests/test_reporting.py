import unittest
from mock import Mock
from tests.ditest import DependencyInjectionTestBase

class ReportingTests(DependencyInjectionTestBase):

    def setUp(self):
        super(ReportingTests, self).setUp()

    def report(self, *args, **kwargs):
        import niprov
        return niprov.report(*args, dependencies=self.dependencies, **kwargs)

    def test_Without_specifics_returns_all_files(self):
        out = self.report()
        self.exporter.export.assert_called_with(self.repo.all())
        self.assertEqual(out, self.exporter.export())

    def test_Can_report_on_one_file_specifically(self):
        out = self.report(forFile='afile.f')
        self.exporter.export.assert_called_with(self.repo.byLocation('afile.f'))
        self.assertEqual(out, self.exporter.export())

    def test_Completes_locationString_forFile(self):
        out = self.report(forFile='afile.f')
        self.locationFactory.completeString.assert_any_call('afile.f')
        self.repo.byLocation.assert_called_with(self.locationFactory.completeString())

    def test_Can_report_on_all_files_for_subject(self):
        out = self.report(forSubject='Jane Doe')
        self.exporter.export.assert_called_with(
            self.repo.bySubject('Jane Doe'))
        self.assertEqual(out, self.exporter.export())

    def test_Obtains_exporter_from_factory(self):
        self.report()
        self.exportFactory.createExporter.assert_any_call(None, None)
        self.report(medium='html')
        self.exportFactory.createExporter.assert_any_call('html', None)
        self.report(form='narrative')
        self.exportFactory.createExporter.assert_any_call(None, 'narrative')

    def test_Passes_provenance_to_exporter(self):
        self.report()
        self.exportFactory.createExporter().export.assert_any_call(self.repo.all())
        self.report(forSubject='Jane')
        self.exportFactory.createExporter().export.assert_any_call(self.repo.bySubject())

    def test_Passes_single_item_of_provenance_to_exporter(self):
        self.report(forFile='xyz')
        self.exportFactory.createExporter().export.assert_any_call(
            self.repo.byLocation('xyz'))

    def test_If_file_unknown_tells_listener(self):
        self.locationFactory.completeString.side_effect = lambda p: p
        self.repo.knowsByLocation.return_value = False
        self.repo.byLocation.side_effect = IndexError
        self.report(forFile='xyz')
        self.listener.unknownFile.assert_called_with('xyz')

    def test_Can_report_on_stats(self):
        out = self.report(statistics=True)
        self.exporter.export.assert_called_with(self.repo.statistics())
        self.assertEqual(out, self.exporter.export())



