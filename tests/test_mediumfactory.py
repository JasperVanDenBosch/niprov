from mock import Mock, patch, call
from tests.ditest import DependencyInjectionTestBase


class MediumFactoryTests(DependencyInjectionTestBase):

    def setUp(self):
        super(MediumFactoryTests, self).setUp()

    def test_Provides_stdout(self):
        from niprov.mediumfactory import MediumFactory
        from niprov.stdout import StandardOutputExporter
        factory = MediumFactory()
        self.assertIsInstance(factory.create('stdout'), StandardOutputExporter)




