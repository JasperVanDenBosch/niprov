from unittest import TestCase
from tests.ditest import DependencyInjectionTestBase
from mock import Mock, patch, sentinel
import numpy


class CameraTests(DependencyInjectionTestBase):

    def test_saveSnapshot(self):
        from niprov.camera import Camera
        camera = Camera(self.dependencies)
        camera.takeSnapshot = Mock()
        target = Mock()
        camera.saveSnapshot(target, for_=sentinel.object)
        newPicture = self.pictureCache.new()
        camera.takeSnapshot.assert_called_with(target, on=newPicture)
        self.pictureCache.keep.assert_called_with(newPicture, sentinel.object)

    def test_SaveSnapshot_doesnt_save_if_takeSnapshot_failed(self):
        from niprov.camera import Camera
        camera = Camera(self.dependencies)
        camera.takeSnapshot = Mock()
        camera.takeSnapshot.return_value = False
        target = Mock()
        camera.saveSnapshot(target, for_=sentinel.object)
        self.assertFalse(self.pictureCache.keep.called)

    def test_If_no_matplotlib_installed_takeSnapshot_returns_false(self):
        from niprov.camera import Camera
        camera = Camera(self.dependencies)
        self.libs.hasDependency.return_value = False
        self.libs.pyplot = None
        self.assertFalse(camera.takeSnapshot(numpy.zeros([3,3,3]), Mock()))

    def test_If_exception_during_plotting_returns_False(self):
        from niprov.camera import Camera
        camera = Camera(self.dependencies)
        self.libs.pyplot.subplots.side_effect = ValueError
        self.assertFalse(camera.takeSnapshot(numpy.zeros([3,3,3]), Mock()))

    def test_If_no_exception_during_plotting_returns_True(self):
        from niprov.camera import Camera
        camera = Camera(self.dependencies)
        self.libs.pyplot.subplots.return_value = [Mock(), [Mock()]*3]
        self.assertTrue(camera.takeSnapshot(numpy.zeros([3,3,3]), Mock()))

    def test_If_interactive_mode_is_on_temporarily_switches_it_off(self):
        from niprov.camera import Camera
        camera = Camera(self.dependencies)
        self.libs.pyplot.isinteractive.return_value = True
        camera.takeSnapshot(numpy.zeros([3,3,3]), Mock())
        self.libs.pyplot.ioff.assert_called_with()

    def test_Interactive_mode_switched_back_on_even_if_exception_thrown(self):
        from niprov.camera import Camera
        camera = Camera(self.dependencies)
        self.libs.pyplot.isinteractive.return_value = True
        self.libs.pyplot.subplots.side_effect = ValueError
        camera.takeSnapshot(numpy.zeros([3,3,3]), Mock())
        self.libs.pyplot.ion.assert_called_with()

    def test_If_interactive_mode_is_off_leave_it_off(self):
        from niprov.camera import Camera
        camera = Camera(self.dependencies)
        self.libs.pyplot.isinteractive.return_value = False
        camera.takeSnapshot(numpy.zeros([3,3,3]), Mock())
        assert not self.libs.pyplot.ion.called



