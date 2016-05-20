from unittest import TestCase
from mock import Mock, sentinel, patch


class PictureCacheTests(TestCase):

    def test_Serialize(self):
        from niprov.pictures import PictureCache
        pictures = PictureCache(sentinel.dependencies)
        pictures.serializeSingle(sentinel.img)

    def test_Provides_new_picture_file_handle(self):
        # new()
        pass

    def test_Stored_picture_can_be_retrieved_as_filepath(self):
        # keep(fhandle) - > serialize() / getPictureFilepathFor()
        pass

    def test_Stored_picture_can_be_retrieved_as_bytes(self):
        # keep(fhandle) - > getPictureDataFor()
        pass

    def test_Can_be_told_to_persist_picture_to_disk_now(self):
        # savePictureToDiskFor()
        pass

