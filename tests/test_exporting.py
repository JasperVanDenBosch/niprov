import unittest
from mock import sentinel
from tests.ditest import DependencyInjectionTestBase

class ExportingTests(DependencyInjectionTestBase):

    def setUp(self):
        super(ExportingTests, self).setUp()

    def export(self, *args, **kwargs):
        import niprov
        return niprov.export(*args, dependencies=self.dependencies, **kwargs)

    def test_Obtains_format_from_factory(self):
        self.export(form='json', medium='x')
        self.formatFactory.create.assert_any_call('json')
        self.export(form='xml', medium='x')
        self.formatFactory.create.assert_any_call('xml')

    def test_Obtains_medium_from_factory(self):
        self.export(medium='file', form='x')
        self.mediumFactory.create.assert_any_call('file')
        self.export(medium='stdout', form='x')
        self.mediumFactory.create.assert_any_call('stdout')

    def test_Passes_provenance_through_format_and_medium(self):
        self.format.serialize.return_value = 'serialized prov'
        self.medium.export.return_value = sentinel.mediumOutput
        out = self.export('a medium','a format')
        self.format.serialize.assert_any_call(self.repo.latest())
        self.medium.export.assert_called_with('serialized prov')
        self.assertEqual(sentinel.mediumOutput, out)

    def test_Without_specifics_returns_latest_files(self):
        out = self.export('a medium','a format')
        self.format.serialize.assert_called_with(self.repo.latest())

    def test_Can_export_one_file_specifically(self):
        out = self.export('a medium','a format',forFile='afile.f')
        self.format.serialize.assert_called_with(self.repo.byLocation('afile.f'))

    def test_Can_export_all_files_for_subject(self):
        out = self.export('a medium','a format',forSubject='Jane Doe')
        self.format.serialize.assert_called_with(
            self.repo.bySubject('Jane Doe'))

    def test_Passes_single_item_of_provenance_to_exporter(self):
        self.export('a medium','a format',forFile='xyz')
        self.format.serialize.assert_any_call(
            self.repo.byLocation('xyz'))

    def test_Can_export_stats(self):
        out = self.export('a medium','a format',statistics=True)
        self.format.serialize.assert_called_with(self.repo.statistics())

    def test_Completes_locationString_forFile(self):
        out = self.export('a medium','a format',forFile='afile.f')
        self.locationFactory.completeString.assert_any_call('afile.f')
        self.repo.byLocation.assert_called_with(self.locationFactory.completeString())

    def test_If_file_unknown_tells_listener(self):
        self.locationFactory.completeString.side_effect = lambda p: p
        self.repo.knowsByLocation.return_value = False
        self.repo.byLocation.side_effect = IndexError
        self.export('a medium','a format',forFile='xyz')
        self.listener.unknownFile.assert_called_with('xyz')

    def test_Can_export_pipeline_for_file(self):
        out = self.export('a medium','a format', forFile='a/b/c', pipeline=True)
        self.pipelineFactory.forFile.assert_called_with(self.repo.byLocation())
        self.format.serialize.assert_called_with(
            self.pipelineFactory.forFile())




