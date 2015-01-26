import unittest
from mock import Mock
from datetime import datetime as dt


class loggingTests(unittest.TestCase):

    def test_Returns_provenance(self):
        from niprov.logging import log
        repo = Mock()
        repo.knowsByPath.return_value = False
        parent = '/p/f1'
        new = '/p/f2'
        trans = 'Something cool'
        provenance = log(trans, parent, new, repository=repo)
        self.assertEqual(provenance['parent'], parent)
        self.assertEqual(provenance['path'], new)
        self.assertEqual(provenance['transformation'], trans)

    def test_Stores_provenance(self):
        from niprov.logging import log
        repo = Mock()
        repo.knowsByPath.return_value = False
        provenance = log('trans', 'old', 'new', repository=repo)
        repo.add.assert_any_call(provenance)

    def test_Copies_fields_from_known_parent(self):
        from niprov.logging import log
        parent = '/p/f1'
        parentProv = {'acquired':dt.now(),'subject':'JB','protocol':'T3'}
        repo = Mock()
        repo.byPath.side_effect = lambda x: {parent:parentProv}[x]
        provenance = log('trans', parent, 'new', repository=repo)
        self.assertEqual(provenance['acquired'], parentProv['acquired'])
        self.assertEqual(provenance['subject'], parentProv['subject'])
        self.assertEqual(provenance['protocol'], parentProv['protocol'])

    def test_Adds_code_or_logtext(self):
        from niprov.logging import log
        repo = Mock()
        repo.knowsByPath.return_value = False
        provenance = log('trans', 'old', 'new', code='abc', logtext='def', repository=repo)
        repo.add.assert_any_call(provenance)
        self.assertEqual(provenance['code'],'abc')
        self.assertEqual(provenance['logtext'],'def')

        

