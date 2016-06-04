from unittest import TestCase
from tests.ditest import DependencyInjectionTestBase
from mock import Mock, patch, sentinel


class CameraTests(DependencyInjectionTestBase):

    def test_saveSnapshot(self):
        from niprov.camera import Camera
        camera = Camera(self.dependencies)
        camera.takeSnapshot = Mock()
        target = Mock()
        camera.saveSnapshot(target, for_=sentinel.object)
        newPicture = self.pictureCache.new()
        camera.takeSnapshot.assert_called_with(target, on=newPicture)
        self.pictureCache.keep.assert_called_with(newPicture, for_=sentinel.object)



