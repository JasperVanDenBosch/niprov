import unittest
from mock import Mock


class DependencyInjectionTestBase(unittest.TestCase):

    def setUp(self):
        self.config = Mock()
        self.listener = Mock()
        self.hasher = Mock()
        self.filesys = Mock()
        self.json = Mock()
        self.repo = Mock()
        self.exporter = Mock()
        self.exportFactory = Mock()
        self.exportFactory.createExporter.return_value = self.exporter
        self.fileFactory = Mock()
        self.serializer = Mock()
        self.location = Mock()
        self.clock = Mock()
        self.locationFactory = Mock()
        self.locationFactory.fromString.return_value = self.location
        self.dependencies = Mock()
        self.dependencies.getLocationFactory.return_value = self.locationFactory
        self.dependencies.getListener.return_value = self.listener
        self.dependencies.getHasher.return_value = self.hasher
        self.dependencies.getFilesystem.return_value = self.filesys
        self.dependencies.getSerializer.return_value = self.json
        self.dependencies.getRepository.return_value = self.repo
        self.dependencies.getFileFactory.return_value = self.fileFactory
        self.dependencies.getSerializer.return_value = self.serializer
        self.dependencies.getExportFactory.return_value = self.exportFactory
        self.dependencies.getConfiguration.return_value = self.config
        self.dependencies.getClock.return_value = self.clock


