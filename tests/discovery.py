import unittest

class DiscoveryTests(unittest.TestCase):

    def test_one(self):
        import niprov
        niprov.discover()
