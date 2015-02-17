import unittest
from mock import Mock
from datetime import datetime

class BasicInspectionTests(unittest.TestCase):

    def setUp(self):
        self.log = Mock()
        self.hasher = Mock()
        self.filesys = Mock()
        self.json = Mock()
        self.path = 'example.abc'
        from niprov.basefile import BaseFile
        self.file = BaseFile(self.path, listener=self.log, 
            filesystem=self.filesys, hasher=self.hasher, serializer=self.json)

    def test_Saves_file_path_along_with_provenance(self):
        out = self.file.inspect()
        self.assertEqual(out['path'], self.path)

    def test_Saves_filesize_along_with_provenance(self):
        out = self.file.inspect()
        self.assertEqual(out['size'], self.filesys.getsize(self.path))

    def test_Saves_file_creation_time_along_with_provenance(self):
        out = self.file.inspect()
        self.assertEqual(out['created'], self.filesys.getctime(self.path))

    def test_Asks_hasher_for_digest_of_file(self):
        out = self.file.inspect()
        self.assertEqual(out['hash'], self.hasher.digest(self.path))

    def test_Attach_method(self):
        self.file.provenance = {'foo':'bar'}
        self.file.attach()
        self.json.serialize.assert_called_with(self.file.provenance)
        self.filesys.write.assert_called_with(
            self.path+'.provenance', self.json.serialize(self.file.provenance))


#ATTACH
# check if we have provenance to attach
# call method for type-specific attachment behavior (file or insert)



#READATTACHED
# call method for type-specific attachment behavior (file or insert)
# return provenance
# save provenance to instance
