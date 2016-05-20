from unittest import TestCase
from mock import Mock, sentinel, patch


class PictureCacheTests(TestCase):

    def test_Serialize(self):
        from niprov.pictures import PictureCache
        pictures = PictureCache(sentinel.dependencies)
        pictures.serializeSingle(sentinel.img)

    def test_Provides_new_picture_file_handle(self):
        pass

    def test_Stored_picture_can_be_retrieved_as_filepath(self):
        # store(fhandle) - > serialize() / getPictureFilepathFor()
        pass

    def test_Stored_picture_can_be_retrieved_as_bytes(self):
        # store(fhandle) - > getPictureDataFor()
        pass

