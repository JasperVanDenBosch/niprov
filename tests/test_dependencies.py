import unittest
import mock
from mock import Mock, patch


class DependenciesTests(unittest.TestCase):

    def setUp(self):
        pass

    def test_Changing_setting_directly_affects_component_setting(self):
        from niprov.dependencies import Dependencies
        dependencies = Dependencies()
        self.assertEqual(dependencies.getListener().verbosity, 'info')
        dependencies.config.verbosity = 'warning'
        self.assertEqual(dependencies.getListener().verbosity, 'warning')

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
        self.assertEqual(dependencies.getListener().verbosity, 'info')
        dependencies.reconfigureOrGetConfiguration(None)
        self.assertEqual(dependencies.getListener().verbosity, 'info')

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
        self.assertEqual(dependencies.getListener().verbosity, 'info')
        newSettings = Configuration()
        newSettings.verbosity = 'warning'
        dependencies.reconfigureOrGetConfiguration(newSettings)
        self.assertEqual(dependencies.getListener().verbosity, 'warning')

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

    def test_provides_PipelineFactory(self):
        from niprov.dependencies import Dependencies
        from niprov.pipelinefactory import PipelineFactory
        dependencies = Dependencies()
        self.assertIsInstance(dependencies.getPipelineFactory(), 
            PipelineFactory)

    def test_provides_FormatFactory(self):
        from niprov.dependencies import Dependencies
        from niprov.formatfactory import FormatFactory
        dependencies = Dependencies()
        self.assertIsInstance(dependencies.getFormatFactory(), 
            FormatFactory)

    def test_provides_MediumFactory(self):
        from niprov.dependencies import Dependencies
        from niprov.mediumfactory import MediumFactory
        dependencies = Dependencies()
        self.assertIsInstance(dependencies.getMediumFactory(), 
            MediumFactory)

    def test_provides_Externals(self):
        from niprov.dependencies import Dependencies
        from niprov.externals import Externals
        dependencies = Dependencies()
        self.assertIsInstance(dependencies.getExternals(), 
            Externals)

    def test_provides_FileFilter(self):
        from niprov.dependencies import Dependencies
        from niprov.filefilter import FileFilter
        dependencies = Dependencies()
        self.assertIsInstance(dependencies.getFileFilter(), 
            FileFilter)

    def test_provides_Hasher(self):
        from niprov.dependencies import Dependencies
        from niprov.hashing import Hasher
        dependencies = Dependencies()
        self.assertIsInstance(dependencies.getHasher(), 
            Hasher)

    def test_provides_Users(self):
        from niprov.dependencies import Dependencies
        from niprov.users import Users
        dependencies = Dependencies()
        self.assertIsInstance(dependencies.getUsers(), 
            Users)

    def test_provides_Camera(self):
        from niprov.dependencies import Dependencies
        from niprov.camera import Camera
        dependencies = Dependencies()
        self.assertIsInstance(dependencies.getCamera(), 
            Camera)

    def test_provides_PictureCache(self):
        from niprov.dependencies import Dependencies
        from niprov.pictures import PictureCache
        dependencies = Dependencies()
        self.assertIsInstance(dependencies.getPictureCache(), 
            PictureCache)

    def test_provides_Query(self):
        from niprov.dependencies import Dependencies
        from niprov.querying import Query
        dependencies = Dependencies()
        self.assertIsInstance(dependencies.getQuery(), Query)

