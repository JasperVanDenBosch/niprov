import unittest
from mock import Mock


class addTests(unittest.TestCase):

    def test_Returns_provenance(self):
        from niprov.adding import add
        repo = Mock()
        new = '/p/f2'
        provenance = add(new, repository=repo)
        self.assertEqual(provenance['path'], new)
        self.assertEqual(provenance['transient'], False)

    def test_Stores_provenance(self):
        from niprov.adding import add
        repo = Mock()
        new = '/p/f2'
        provenance = add(new, repository=repo)
        repo.add.assert_any_call(provenance)

        

