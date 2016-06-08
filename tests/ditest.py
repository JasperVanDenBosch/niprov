import unittest
from mock import Mock


class DependencyInjectionTestBase(unittest.TestCase):

    def setUp(self):
        self.config = Mock()
        self.pipelineFactory = Mock()
        self.listener = Mock()
        self.hasher = Mock()
        self.filesys = Mock()
        self.repo = Mock()
        self.fileFactory = Mock()
        self.serializer = Mock()
        self.location = Mock()
        self.clock = Mock()
        self.formatFactory = Mock()
        self.format = Mock()
        self.format.fileExtension = 'txt'
        self.formatFactory.create.return_value = self.format
        self.medium = Mock()
        self.mediumFactory = Mock()
        self.mediumFactory.create.return_value = self.medium
        self.locationFactory = Mock()
        self.locationFactory.fromString.return_value = self.location
        self.users = Mock()
        self.camera = Mock()
        self.libs = Mock()
        self.pictureCache = Mock()
        self.query = Mock()
        self.dependencies = Mock()
        self.dependencies.getQuery.return_value = self.query
        self.dependencies.getLibraries.return_value = self.libs
        self.dependencies.getCamera.return_value = self.camera
        self.dependencies.getPictureCache.return_value = self.pictureCache
        self.dependencies.getUsers.return_value = self.users
        self.dependencies.getLocationFactory.return_value = self.locationFactory
        self.dependencies.getListener.return_value = self.listener
        self.dependencies.getHasher.return_value = self.hasher
        self.dependencies.getFilesystem.return_value = self.filesys
        self.dependencies.getRepository.return_value = self.repo
        self.dependencies.getFileFactory.return_value = self.fileFactory
        self.dependencies.getSerializer.return_value = self.serializer
        self.dependencies.getConfiguration.return_value = self.config
        self.dependencies.getClock.return_value = self.clock
        self.dependencies.getPipelineFactory.return_value = self.pipelineFactory
        self.dependencies.getFormatFactory.return_value = self.formatFactory
        self.dependencies.getMediumFactory.return_value = self.mediumFactory


