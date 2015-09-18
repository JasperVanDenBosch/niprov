import unittest
from mock import Mock


class DependencyInjectionTestBase(unittest.TestCase):

    def setUp(self):
        self.listener = Mock()
        self.hasher = Mock()
        self.filesys = Mock()
        self.json = Mock()
        self.repo = Mock()
        self.fileFactory = Mock()
        self.location = Mock()
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




        

