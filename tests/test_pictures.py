from unittest import TestCase
from mock import Mock, sentinel, patch
import io, os, shutil, bson


class PictureCacheTests(TestCase):

    def setUp(self):
        picdir = os.path.expanduser('~/.niprov-snapshots')
        if os.path.isdir(picdir):
            shutil.rmtree(picdir)
        import niprov.pictures
        niprov.pictures._CACHE = {} # reset cache

    def test_Serialize(self):
        from niprov.pictures import PictureCache
        pictures = PictureCache(sentinel.dependencies)
        pictures.getFilepath = Mock()
        fpath = pictures.serializeSingle(sentinel.img)
        pictures.getFilepath.assert_called_with(for_=sentinel.img)
        self.assertEqual(pictures.getFilepath(), fpath)

    def test_Provides_new_picture_file_handle(self):
        from niprov.pictures import PictureCache
        pictures = PictureCache(sentinel.dependencies)
        newPicture = pictures.new()
        self.assertTrue(hasattr(newPicture, 'write'))

    def test_Stored_picture_can_be_retrieved_as_filepath(self):
        from niprov.pictures import PictureCache
        myImg = Mock()
        myImg.provenance = {'id':'007'}
        pictures = PictureCache(sentinel.dependencies)
        self.assertIsNone(pictures.getFilepath(for_=myImg))
        pictures.keep(io.BytesIO('/x10/x05/x5f'), for_=myImg)
        picfpath = os.path.expanduser('~/.niprov-snapshots/007.png')
        self.assertEqual(picfpath, pictures.getFilepath(for_=myImg))

    def test_Stored_picture_can_be_retrieved_as_bytes(self):
        from niprov.pictures import PictureCache
        myImg = Mock()
        myImg.provenance = {'id':'007'}
        pictures = PictureCache(sentinel.dependencies)
        newPicture = pictures.new()
        newPicture.write('/x10/x05/x5f')
        pictures.keep(newPicture, for_=myImg)
        outBytes = pictures.getBytes(for_=myImg)
        self.assertEqual('/x10/x05/x5f', outBytes)

    def test_Can_be_told_to_persist_picture_to_disk_now(self):
        from niprov.pictures import PictureCache
        myImg = Mock()
        myImg.provenance = {'id':'007'}
        pictures = PictureCache(sentinel.dependencies)
        pictures.saveToDisk(for_=myImg) #shouldn't do anything
        pictures.keep(io.BytesIO('/x10/x05/x5f'), for_=myImg)
        pictures.saveToDisk(for_=myImg)
        picfpath = os.path.expanduser('~/.niprov-snapshots/007.png')
        self.assertTrue(os.path.isfile(picfpath))
        with open(picfpath) as picFile:
            self.assertEqual(picFile.read(), '/x10/x05/x5f')

    def test_If_pic_is_not_in_cache_but_on_filesystem_provides_that(self):
        import niprov.pictures
        myImg = Mock()
        myImg.provenance = {'id':'007'}
        pictures = niprov.pictures.PictureCache(sentinel.dependencies)
        pictures.keep(io.BytesIO('/x10/x05/x5f'), for_=myImg)
        pictures.saveToDisk(for_=myImg)
        niprov.pictures._CACHE = {} # reset cache
        picfpath = os.path.expanduser('~/.niprov-snapshots/007.png')
        self.assertEqual(picfpath, pictures.getFilepath(for_=myImg))

    def test_Keep_accepts_bsonBinary(self):
        from niprov.pictures import PictureCache
        myImg = Mock()
        myImg.provenance = {'id':'007'}
        pictures = PictureCache(sentinel.dependencies)
        pictures.keep(bson.Binary('/x10/x05/x5f'), for_=myImg)
        self.assertEqual('/x10/x05/x5f', pictures.getBytes(for_=myImg))
        
    

