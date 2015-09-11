import unittest
import mock
from mock import Mock


class ContextTests(unittest.TestCase):

    def setUp(self):
        pass

    def test_Changing_setting_directly_affects_component_setting(self):
        from niprov import Context
        context = Context()
        self.assertFalse(context.getListener().settings.verbose)
        context.config.verbose = True
        self.assertTrue(context.getListener().settings.verbose)

    def test_Changing_storage_setting_changes_repository_provided(self):
        from niprov import Context
        from niprov.jsonfile import JsonFile
        from niprov.mongo import MongoRepository
        context = Context()
        self.assertIsInstance(context.getRepository(), JsonFile)
        context.config.database_type = 'MongoDB'
        self.assertIsInstance(context.getRepository(), MongoRepository)

    def test_Reconfigure_with_None_does_nothing(self):
        from niprov import Context
        context = Context()
        self.assertFalse(context.getListener().settings.verbose)
        context.reconfigure(None)
        self.assertFalse(context.getListener().settings.verbose)

    def test_Reconfigure_creates_new_libraries_with_new_Configuration(self):
        from niprov import Context, Configuration
        context = Context()
        self.assertFalse(context.getListener().settings.verbose)
        newSettings = Configuration()
        newSettings.verbose = True
        context.reconfigure(newSettings)
        self.assertTrue(context.getListener().settings.verbose)

    def test_Filefactory_provided(self):
        from niprov import Context
        from niprov.files import FileFactory
        context = Context()
        self.assertIsInstance(context.getFileFactory(), FileFactory)

