import unittest
from mock import Mock
from datetime import datetime as dt


class loggingTests(unittest.TestCase):

    def setUp(self):
        self.repo = Mock()
        self.repo.knowsByPath.return_value = True
        img = Mock()
        img.provenance = {'acquired':dt.now(),'subject':'JD', 'protocol':'X'}
        self.repo.byPath.return_value = img
        self.filesys = Mock()
        self.listener = Mock()
        self.factory = Mock()
        self.newimg = Mock()
        self.provenancesCreated = []
        def wrapProv(p):
            self.provenancesCreated.append(p)
            return self.newimg
        self.factory.fromProvenance.side_effect = lambda p : wrapProv(p)

    def log(self, *args, **kwargs):
        from niprov.logging import log
        return log(*args, repository=self.repo, filesys=self.filesys, 
            listener=self.listener, factory=self.factory, **kwargs)

    def test_Returns_img(self):
        parents = ['/p/f1']
        new = '/p/f2'
        trans = 'Something cool'
        out = self.log(new, trans, parents)
        self.assertEqual(out, self.newimg)

    def test_Stores_provenance(self):
        provenance = self.log('new', 'trans', 'old')
        self.repo.add.assert_any_call(self.newimg.provenance)

    def test_Copies_fields_from_known_parent(self):
        parent = '/p/f1'
        parents = [parent]
        parentProv = {'acquired':dt.now(),'subject':'JB','protocol':'T3'}
        parentImg = Mock()
        parentImg.provenance = parentProv
        self.repo.byPath.side_effect = lambda x: {parent:parentImg}[x]
        self.log('new', 'trans', parents)
        self.assertEqual(self.provenancesCreated[0]['acquired'], parentProv['acquired'])
        self.assertEqual(self.provenancesCreated[0]['subject'], parentProv['subject'])
        self.assertEqual(self.provenancesCreated[0]['protocol'], parentProv['protocol'])

    def test_Adds_code_or_logtext(self):
        self.log('new', 'trans', 'old', code='abc', logtext='def')
        self.assertEqual(self.provenancesCreated[0]['code'],'abc')
        self.assertEqual(self.provenancesCreated[0]['logtext'],'def')

    def test_Accepts_temp_flag(self):
        parents = ['/p/f1']
        new = '/p/f2'
        trans = 'Something cool'
        self.log(new, trans, parents, transient=True)
        self.assertEqual(self.provenancesCreated[0]['transient'], True)

    def test_If_file_doesnt_exists_tells_listener_and_doesnt_save_prov(self):
        self.filesys.fileExists.return_value = False
        parents = ['/p/f1']
        new = '/p/f2'
        trans = 'Something cool'
        self.assertRaises(IOError, self.log, new, trans, parents)
        assert not self.repo.add.called

    def test_For_nonexisting_transient_file_behaves_normal(self):
        self.filesys.fileExists.return_value = False
        parents = ['/p/f1']
        new = '/p/f2'
        trans = 'Something cool'
        self.log(new, trans, parents, transient=True)
        self.assertEqual(self.provenancesCreated[0]['transformation'], trans)

    def test_Can_pass_multiple_new_files(self):
        parents = ['/p/f1']
        new = ['/p/f2','/p/f3']
        trans = 'Something cool'
        self.log(new, trans, parents)
        self.assertEqual(self.provenancesCreated[0]['parents'], parents)
        self.assertEqual(self.provenancesCreated[1]['parents'], parents)
        self.assertEqual(self.provenancesCreated[0]['path'], new[0])
        self.assertEqual(self.provenancesCreated[1]['path'], new[1])

    def test_Script_added_to_provenance(self):
        parents = ['/p/f1']
        new = '/p/f2'
        trans = 'Something cool'
        script = '/p/test.py'
        self.log(new, trans, parents, script=script)
        self.assertEqual(self.provenancesCreated[0]['script'], script)

    def test_Accepts_and_processes_custom_provenance(self):
        parents = ['/p/f1']
        new = '/p/f2'
        trans = 'Something cool'
        p = {'akey':'avalue'}
        self.log(new, trans, parents, provenance=p)
        self.assertEqual(self.provenancesCreated[0]['akey'], 'avalue')

    def test_Notifies_listener_and_exits_if_parent_unknown(self):
        self.repo.knowsByPath.return_value = False
        parent = '/p/f1'
        parents = [parent]
        provenance = self.log('new', 'trans', parents)
        self.listener.unknownFile.assert_called_with(parent)
        assert not self.repo.add.called

    def test_Doesnt_complain_if_parent_is_missing_basic_fields(self):
        img = Mock()
        img.provenance = {'acquired':dt.now()} #missing subject
        self.repo.byPath.return_value = img
        provenance = self.log('new', 'trans', ['/p/f1parent'])
        self.assertNotIn('subject', self.provenancesCreated[0])

    def test_Inspects_nontransient_new_files(self):
        parents = ['/p/f1']
        new = ['/p/f2','/p/f3']
        trans = 'Something cool'
        provenance = self.log(new, trans, parents, transient=True)
        assert not self.newimg.inspect.called
        provenance = self.log(new, trans, parents)
        self.newimg.inspect.assert_called_with()

