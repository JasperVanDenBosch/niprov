from mock import Mock, patch, call
from tests.ditest import DependencyInjectionTestBase


class MediumFactoryTests(DependencyInjectionTestBase):

    def setUp(self):
        super(MediumFactoryTests, self).setUp()

    def test_Provides_stdout(self):
        from niprov.mediumfactory import MediumFactory
        from niprov.mediumstdout import StandardOutputMedium
        factory = MediumFactory()
        self.assertIsInstance(factory.create('stdout'), StandardOutputMedium)

    def test_Provides_direct(self):
        from niprov.mediumfactory import MediumFactory
        from niprov.mediumdirect import DirectMedium
        factory = MediumFactory()
        self.assertIsInstance(factory.create('direct'), DirectMedium)

    def test_Provides_file(self):
        from niprov.mediumfactory import MediumFactory
        from niprov.mediumfile import FileMedium
        factory = MediumFactory()
        self.assertIsInstance(factory.create('file'), FileMedium)

    def test_Raises_exception_on_unknown_name(self):
        from niprov.mediumfactory import MediumFactory
        factory = MediumFactory()
        with self.assertRaisesRegexp(ValueError, 'Unknown medium: poetry'):
           factory.create('poetry')

    def test_Provides_Viewer(self):
        from niprov.mediumfactory import MediumFactory
        from niprov.mediumviewer import ViewerMedium
        factory = MediumFactory()
        self.assertIsInstance(factory.create('viewer'), ViewerMedium)




