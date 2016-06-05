from mock import Mock, patch, call
from tests.ditest import DependencyInjectionTestBase


class FormatFactoryTests(DependencyInjectionTestBase):

    def setUp(self):
        super(FormatFactoryTests, self).setUp()

    def test_Provides_json(self):
        from niprov.formatfactory import FormatFactory
        from niprov.formatjson import JsonFormat
        factory = FormatFactory()
        self.assertIsInstance(factory.create('json'), JsonFormat)

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

    def test_Provides_simple(self):
        from niprov.formatfactory import FormatFactory
        from niprov.formatsimple import SimpleFormat
        factory = FormatFactory()
        self.assertIsInstance(factory.create('simple'), SimpleFormat)

    def test_Provides_dict(self):
        from niprov.formatfactory import FormatFactory
        from niprov.formatdict import DictFormat
        factory = FormatFactory()
        self.assertIsInstance(factory.create('dict'), DictFormat)

    def test_Provides_object(self):
        from niprov.formatfactory import FormatFactory
        from niprov.formatobject import ObjectFormat
        factory = FormatFactory()
        self.assertIsInstance(factory.create('object'), ObjectFormat)

    def test_Provides_picture(self):
        from niprov.formatfactory import FormatFactory
        from niprov.pictures import PictureCache
        factory = FormatFactory()
        self.assertIsInstance(factory.create('picture'), PictureCache)

    def test_Raises_exception_on_unknown_name(self):
        from niprov.formatfactory import FormatFactory
        factory = FormatFactory()
        with self.assertRaisesRegexp(ValueError, 'Unknown format: hexameter'):
           factory.create('hexameter')




