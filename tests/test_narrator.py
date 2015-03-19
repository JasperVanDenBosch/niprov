import unittest
from mock import Mock
from datetime import datetime


class NarratorTests(unittest.TestCase):


    def test_File(self):
        from niprov.narrator import Narrator
        img = Mock()
        p = {}
        p['protocol'] = 'T1'
        p['acquired'] = datetime(2013, 9, 7, 11, 27, 34)
        p['subject'] = 'John Doe'
        p['size'] = 345123
        img.provenance = p
        storyteller = Narrator()
        self.assertEqual(storyteller.narrate(img), ("This is a T1 image. "
            "It was recorded September 7, 2013. "
            "The participant's name is John Doe. "
            "It is 345KB in size. "))
        
