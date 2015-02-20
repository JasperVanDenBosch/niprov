import unittest
from mock import Mock
from datetime import datetime as dt


class loggingTests(unittest.TestCase):

    def setUp(self):
        self.repo = Mock()
        self.repo.knowsByPath.return_value = False
        self.filesys = Mock()

    def log(self, *args, **kwargs):
        from niprov.logging import log
        return log(*args, repository=self.repo, filesys=self.filesys, **kwargs)

    def test_Returns_provenance(self):
        from niprov.logging import log
        self.repo = Mock()
        self.repo.knowsByPath.return_value = False
        parents = ['/p/f1']
        new = '/p/f2'
        trans = 'Something cool'
        provenance = self.log(new, trans, parents)
        self.assertEqual(provenance['parents'], parents)
        self.assertEqual(provenance['path'], new)
        self.assertEqual(provenance['transformation'], trans)

    def test_Stores_provenance(self):
        self.repo.knowsByPath.return_value = False
        provenance = self.log('new', 'trans', 'old')
        self.repo.add.assert_any_call(provenance)

    def test_Copies_fields_from_known_parent(self):
        self.repo.knowsByPath.return_value = True
        parent = '/p/f1'
        parents = [parent]
        parentProv = {'acquired':dt.now(),'subject':'JB','protocol':'T3'}
        self.repo.byPath.side_effect = lambda x: {parent:parentProv}[x]
        provenance = self.log('new', 'trans', parents)
        self.assertEqual(provenance['acquired'], parentProv['acquired'])
        self.assertEqual(provenance['subject'], parentProv['subject'])
        self.assertEqual(provenance['protocol'], parentProv['protocol'])

    def test_Adds_code_or_logtext(self):
        self.repo.knowsByPath.return_value = False
        provenance = self.log('new', 'trans', 'old', code='abc', logtext='def')
        self.repo.add.assert_any_call(provenance)
        self.assertEqual(provenance['code'],'abc')
        self.assertEqual(provenance['logtext'],'def')

    def test_Accepts_temp_flag(self):
        self.repo.knowsByPath.return_value = False
        parents = ['/p/f1']
        new = '/p/f2'
        trans = 'Something cool'
        provenance = self.log(new, trans, parents, transient=True)
        self.assertEqual(provenance['transient'], True)

    def test_If_file_doesnt_exists_tells_listener_and_doesnt_save_prov(self):
        self.repo.knowsByPath.return_value = False
        self.filesys.fileExists.return_value = False
        parents = ['/p/f1']
        new = '/p/f2'
        trans = 'Something cool'
        self.assertRaises(IOError, self.log, new, trans, parents)
        assert not self.repo.add.called
        

    def test_For_nonexisting_transient_file_behaves_normal(self):
        self.repo.knowsByPath.return_value = False
        self.filesys.fileExists.return_value = False
        parents = ['/p/f1']
        new = '/p/f2'
        trans = 'Something cool'
        provenance = self.log(new, trans, parents, transient=True)
        self.repo.add.assert_any_call(provenance)

    def test_Can_pass_multiple_new_files(self):
        parents = ['/p/f1']
        new = ['/p/f2','/p/f3']
        trans = 'Something cool'
        provenance = self.log(new, trans, parents)
        self.assertEqual(provenance[0]['parents'], parents)
        self.assertEqual(provenance[1]['parents'], parents)
        self.assertEqual(provenance[0]['path'], new[0])
        self.assertEqual(provenance[1]['path'], new[1])
        self.repo.add.assert_any_call(provenance[0])
        self.repo.add.assert_any_call(provenance[1])

    def test_Script_added_to_provenance(self):
        parents = ['/p/f1']
        new = '/p/f2'
        trans = 'Something cool'
        script = '/p/test.py'
        provenance = self.log(new, trans, parents, script=script)
        self.assertEqual(provenance['script'], script)

    def test_Accepts_and_processes_custom_provenance(self):
        parents = ['/p/f1']
        new = '/p/f2'
        trans = 'Something cool'
        p = {'akey':'avalue'}
        provenance = self.log(new, trans, parents, provenance=p)
        self.assertEqual(provenance['akey'], 'avalue')


