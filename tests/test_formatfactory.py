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



