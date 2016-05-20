from unittest import TestCase
from mock import Mock, sentinel, patch


class PictureCacheTests(TestCase):

    def test_Serialize(self):
        from niprov.pictures import PictureCache
        pictures = PictureCache(sentinel.dependencies)
        pictures.serializeSingle(sentinel.img)

