import unittest
from mock import sentinel, Mock
from tests.ditest import DependencyInjectionTestBase

class ExportingTests(DependencyInjectionTestBase):

    def setUp(self):
        super(ExportingTests, self).setUp()

    def export(self, *args, **kwargs):
        import niprov
        return niprov.export(*args, dependencies=self.dependencies, **kwargs)

    def test_Obtains_format_from_factory(self):
        self.export(None, form='json', medium='x')
        self.formatFactory.create.assert_any_call('json')
        self.export(None, form='xml', medium='x')
        self.formatFactory.create.assert_any_call('xml')

    def test_Obtains_medium_from_factory(self):
        self.export(None, medium='file', form='x')
        self.mediumFactory.create.assert_any_call('file')
        self.export(None, medium='stdout', form='x')
        self.mediumFactory.create.assert_any_call('stdout')

    def test_Passes_provenance_through_format_and_medium(self):
        self.format.serialize.return_value = 'serialized prov'
        self.medium.export.return_value = sentinel.mediumOutput
        out = self.export(sentinel.images, 'a medium','a format')
        self.format.serialize.assert_any_call(sentinel.images)
        self.medium.export.assert_called_with('serialized prov', self.format)
        self.assertEqual(sentinel.mediumOutput, out)

    def test_Passes_single_item_of_provenance_to_exporter(self):
        self.export(sentinel.image, 'a medium','a format')
        self.format.serialize.assert_any_call(sentinel.image)

    def test_Can_export_pipeline_for_file(self):
        out = self.export(sentinel.image, 'a medium','a format', pipeline=True)
        self.pipelineFactory.forFile.assert_called_with(sentinel.image)
        self.format.serialize.assert_called_with(
            self.pipelineFactory.forFile())

    def test_Backup_passes_all_images_to_export(self):
        import niprov.exporting
        niprov.exporting.export = Mock()
        niprov.exporting.backup(self.dependencies)
        niprov.exporting.export.assert_called_with(self.query.all(), 
            medium='file', form='json', dependencies=self.dependencies)




