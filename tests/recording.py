import unittest
from mock import Mock


class RecordingTests(unittest.TestCase):

    def test_Returns_provenance(self):
        from niprov.recording import record
        ancestor = '/p/f1'
        new = '/p/f2'
        trans = 'Something cool'
        provenance = record(ancestor, new, trans)
        self.assertEqual(provenance['ancestor'], ancestor)
        self.assertEqual(provenance['path'], new)
        self.assertEqual(provenance['transformation'], trans)

    def test_Stores_provenance(self):
        from niprov.recording import record
        repo = Mock()
        provenance = record('old', 'new', 'trans', repository=repo)
        repo.add.assert_any_call(provenance)

        

