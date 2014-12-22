import unittest
from mock import Mock

class InspectionTests(unittest.TestCase):

    def test_one(self):
        import niprov
        log = Mock()
        niprov.inspect('/p/f1.x', listener=log)


        

