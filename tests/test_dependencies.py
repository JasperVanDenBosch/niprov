import unittest
import mock
from mock import Mock, patch


class DependenciesTests(unittest.TestCase):

    def setUp(self):
        pass

    def test_Changing_setting_directly_affects_component_setting(self):
        from niprov.dependencies import Dependencies
        dependencies = Dependencies()
        self.assertFalse(dependencies.getListener().settings.verbose)
        dependencies.config.verbose = True
        self.assertTrue(dependencies.getListener().settings.verbose)

    def test_Changing_storage_setting_changes_repository_provided(self):
        from niprov.dependencies import Dependencies
        from niprov.jsonfile import JsonFile
        from niprov.mongo import MongoRepository
        dependencies = Dependencies()
        with patch('niprov.mongo.pymongo'):
            dependencies.config.database_type = 'file'
            self.assertIsInstance(dependencies.getRepository(), JsonFile)
            dependencies.config.database_type = 'MongoDB'
            self.assertIsInstance(dependencies.getRepository(), MongoRepository)

    def test_reconfigureOrGetConfiguration_with_None_doesnt_affect_config(self):
        from niprov.dependencies import Dependencies
        dependencies = Dependencies()
        self.assertFalse(dependencies.getListener().settings.verbose)
        dependencies.reconfigureOrGetConfiguration(None)
        self.assertFalse(dependencies.getListener().settings.verbose)

    def test_reconfigureOrGetConfiguration_with_None_returns_config(self):
        from niprov.dependencies import Dependencies
        dependencies = Dependencies()
        outConfig = dependencies.reconfigureOrGetConfiguration(None)
        self.assertEqual(dependencies.config, outConfig)

    def test_reconfigureOrGetConfiguration_with_new_config_returns_it(self):
        from niprov.dependencies import Dependencies, Configuration
        dependencies = Dependencies()
        newSettings = Configuration()
        newSettings.verbose = True
        outConfig = dependencies.reconfigureOrGetConfiguration(newSettings)
        self.assertEqual(newSettings, outConfig)

    def test_reconfigureOrGetConfiguration_creates_new_dependencies(self):
        from niprov.dependencies import Dependencies, Configuration
        dependencies = Dependencies()
        self.assertFalse(dependencies.getListener().settings.verbose)
        newSettings = Configuration()
        newSettings.verbose = True
        dependencies.reconfigureOrGetConfiguration(newSettings)
        self.assertTrue(dependencies.getListener().settings.verbose)

    def test_GetConfiguration_returns_config(self):
        from niprov.dependencies import Dependencies
        dependencies = Dependencies()
        outConfig = dependencies.getConfiguration()
        self.assertEqual(dependencies.config, outConfig)

    def test_Filefactory_provided(self):
        from niprov.dependencies import Dependencies
        from niprov.files import FileFactory
        dependencies = Dependencies()
        self.assertIsInstance(dependencies.getFileFactory(), FileFactory)

    def test_provides_LocationFactory(self):
        from niprov.dependencies import Dependencies
        from niprov.locationfactory import LocationFactory
        dependencies = Dependencies()
        self.assertIsInstance(dependencies.getLocationFactory(), 
            LocationFactory)

