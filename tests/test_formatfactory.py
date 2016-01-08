from mock import Mock, patch, call
from tests.ditest import DependencyInjectionTestBase


class FormatFactoryTests(DependencyInjectionTestBase):

    def setUp(self):
        super(FormatFactoryTests, self).setUp()

    def test_Provides_json(self):
        from niprov.formatfactory import FormatFactory
        from niprov.jsonserializing import JsonSerializer
        factory = FormatFactory()
        self.assertIsInstance(factory.create('json'), JsonSerializer)

    def test_Provides_xml(self):
        from niprov.formatfactory import FormatFactory
        from niprov.formatxml import XmlFormat
        factory = FormatFactory()
        self.assertIsInstance(factory.create('xml'), XmlFormat)

    def test_Provides_narrated(self):
        from niprov.formatfactory import FormatFactory
        from niprov.formatnarrated import NarratedFormat
        factory = FormatFactory()
        self.assertIsInstance(factory.create('narrated'), NarratedFormat)

    def test_Raises_exception_on_unknown_name(self):
        from niprov.formatfactory import FormatFactory
        factory = FormatFactory()
        with self.assertRaisesRegexp(ValueError, 'Unknown format: hexameter'):
           factory.create('hexameter')




