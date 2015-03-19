import unittest
from mock import Mock


class NarratorTests(unittest.TestCase):


    def test_File(self):
        from niprov.narrator import Narrator
        img = Mock()
        p = {}
        p['protocol'] = 'T1'
        img.provenance = p
        storyteller = Narrator()
        self.assertEqual(storyteller.narrate(img), "This is a T1 image.")
        
