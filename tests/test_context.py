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
        context.settings.verbose = True
        self.assertTrue(context.getListener().settings.verbose)

    def test_Changing_storage_setting_changes_repository_provided(self):
        pass

    def test_Reconfigure_with_None_does_nothing(self):
        from niprov import Context
        context = Context()
        self.assertFalse(context.getListener().settings.verbose)
        context.reconfigure(None)
        self.assertFalse(context.getListener().settings.verbose)

    def test_Reconfigure_creates_new_dependencies_with_new_Configuration(self):
        from niprov import Context, Configuration
        context = Context()
        self.assertFalse(context.getListener().settings.verbose)
        newSettings = Configuration()
        newSettings.verbose = True
        context.reconfigure(newSettings)
        self.assertTrue(context.getListener().settings.verbose)
