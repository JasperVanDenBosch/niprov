import unittest
from mock import Mock
from datetime import datetime as dt


class RecordingTests(unittest.TestCase):

    def test_Returns_provenance(self):
        from niprov.recording import record
        repo = Mock()
        repo.knowsByPath.return_value = False
        ancestor = '/p/f1'
        new = '/p/f2'
        trans = 'Something cool'
        provenance = record(trans, ancestor, new, repository=repo)
        self.assertEqual(provenance['ancestor'], ancestor)
        self.assertEqual(provenance['path'], new)
        self.assertEqual(provenance['transformation'], trans)

    def test_Stores_provenance(self):
        from niprov.recording import record
        repo = Mock()
        repo.knowsByPath.return_value = False
        provenance = record('trans', 'old', 'new', repository=repo)
        repo.add.assert_any_call(provenance)

    def test_Copies_fields_from_known_ancestor(self):
        from niprov.recording import record
        ancestor = '/p/f1'
        ancestorProv = {'acquired':dt.now(),'subject':'JB','protocol':'T3'}
        repo = Mock()
        repo.byPath.side_effect = lambda x: {ancestor:ancestorProv}[x]
        provenance = record('trans', ancestor, 'new', repository=repo)
        self.assertEqual(provenance['acquired'], ancestorProv['acquired'])
        self.assertEqual(provenance['subject'], ancestorProv['subject'])
        self.assertEqual(provenance['protocol'], ancestorProv['protocol'])

        

