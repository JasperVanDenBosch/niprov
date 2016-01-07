import unittest
from mock import sentinel
from tests.ditest import DependencyInjectionTestBase

class ReportingTests(DependencyInjectionTestBase):

    def setUp(self):
        super(ReportingTests, self).setUp()

    def report(self, *args, **kwargs):
        import niprov
        return niprov.report(*args, dependencies=self.dependencies, **kwargs)

    def test_Obtains_format_from_factory(self):
        self.report(form='json')
        self.formatFactory.create.assert_any_call('json')
        self.report(form='xml')
        self.formatFactory.create.assert_any_call('xml')

    def test_Obtains_medium_from_factory(self):
        self.report(medium='file')
        self.mediumFactory.create.assert_any_call('file')
        self.report(medium='stdout')
        self.mediumFactory.create.assert_any_call('stdout')

    def test_Passes_provenance_through_format_and_medium(self):
        self.format.serialize.return_value = 'serialized prov'
        self.medium.export.return_value = sentinel.mediumOutput
        out = self.report()
        self.format.serialize.assert_any_call(self.repo.latest())
        self.medium.export.assert_called_with('serialized prov')
        self.assertEqual(sentinel.mediumOutput, out)

    def test_Without_specifics_returns_latest_files(self):
        out = self.report()
        self.format.serialize.assert_called_with(self.repo.latest())

    def test_Can_report_on_one_file_specifically(self):
        out = self.report(forFile='afile.f')
        self.format.serialize.assert_called_with(self.repo.byLocation('afile.f'))

    def test_Can_report_on_all_files_for_subject(self):
        out = self.report(forSubject='Jane Doe')
        self.format.serialize.assert_called_with(
            self.repo.bySubject('Jane Doe'))

    def test_Passes_single_item_of_provenance_to_exporter(self):
        self.report(forFile='xyz')
        self.format.serialize.assert_any_call(
            self.repo.byLocation('xyz'))

    def test_Can_report_on_stats(self):
        out = self.report(statistics=True)
        self.format.serialize.assert_called_with(self.repo.statistics())

    def test_Completes_locationString_forFile(self):
        out = self.report(forFile='afile.f')
        self.locationFactory.completeString.assert_any_call('afile.f')
        self.repo.byLocation.assert_called_with(self.locationFactory.completeString())

    def test_If_file_unknown_tells_listener(self):
        self.locationFactory.completeString.side_effect = lambda p: p
        self.repo.knowsByLocation.return_value = False
        self.repo.byLocation.side_effect = IndexError
        self.report(forFile='xyz')
        self.listener.unknownFile.assert_called_with('xyz')




