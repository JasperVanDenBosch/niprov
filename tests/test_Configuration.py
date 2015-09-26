import unittest
from mock import Mock, patch
import os


class ConfigurationTests(unittest.TestCase):

    def setUp(self):
        self.ospath = Mock()
        self.parser = Mock()
        self.parser.get.side_effect = lambda s, k: 'nothing'

    def createConfiguration(self, configFilePath=None):
        from niprov.config import Configuration
        with patch('niprov.config.os') as osp:
            osp.path = self.ospath
            with patch('niprov.config.ConfigParser') as ConfigParser:
                osp.path.expanduser.side_effect = lambda p: p.replace('~',
                    'user-home-directory')
                ConfigParser.SafeConfigParser.return_value = self.parser
                if configFilePath:
                    conf = Configuration(configFilePath)
                else:
                    conf = Configuration()
        return conf

    def test_If_no_config_file_uses_defaults(self):
        self.ospath.isfile.return_value = False
        conf = self.createConfiguration()
        self.assertEqual(False, conf.verbose)
        self.assertEqual(False, conf.dryrun)

    def test_If_config_file_reads_it(self):
        self.ospath.isfile.return_value = True
        conf = self.createConfiguration()
        self.parser.read.assert_called_with('user-home-directory/niprov.cfg')

    def test_Can_pass_file_location(self):
        self.ospath.isfile.return_value = True
        conf = self.createConfiguration('~/my/path.cfg')
        self.parser.read.assert_called_with('user-home-directory/my/path.cfg')

    def test_Uses_values_in_file(self):
        self.ospath.isfile.return_value = True
        self.parser.getboolean.side_effect = lambda s, k: True
        self.parser.get.side_effect = lambda s, k: 'mothership'
        conf = self.createConfiguration()
        self.assertEqual(True, conf.verbose)
        self.assertEqual('mothership', conf.database_type)

    def test_Can_deal_with_lists(self):
        self.ospath.isfile.return_value = True
        self.parser.get.side_effect = lambda s, k: 'a1,b2, c3,d4 ,'
        conf = self.createConfiguration()
        self.assertEqual(['a1','b2','c3','d4'], conf.discover_file_extensions)

