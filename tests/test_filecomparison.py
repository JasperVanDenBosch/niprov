import unittest
from mock import Mock
import os.path as ospath

class FilecomparisonTests(unittest.TestCase):


    def test_Hasher_provides_unique_hashes(self):
        import niprov.hashing
        hasher = niprov.hashing.Hasher()
        file1 = __file__
        file2 = niprov.hashing.__file__
        self.assertEqual(hasher.digest(file1), hasher.digest(file1))
        self.assertNotEqual(hasher.digest(file1), hasher.digest(file2))
