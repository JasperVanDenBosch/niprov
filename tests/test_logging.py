import unittest
from mock import Mock, sentinel, patch
from datetime import datetime as dt
from tests.ditest import DependencyInjectionTestBase


class LoggingTests(DependencyInjectionTestBase):

    def setUp(self):
        super(LoggingTests, self).setUp()
        self.repo.knowsByLocation.return_value = True
        self.opts = Mock()
        self.opts.dryrun = False
        img = Mock()
        img.provenance = {'acquired':dt.now(),'subject':'JD', 'protocol':'X'}
        self.repo.byLocation.return_value = img
        self.newimg = Mock()
        self.provenancesCreated = []
        def wrapProv(location,transient,provenance,dependencies):
            self.provenancesCreated.append(provenance)
            return self.newimg
        self.dependencies.reconfigureOrGetConfiguration.return_value = self.opts
        patcher = patch('niprov.logging.add')
        self.add = patcher.start()
        self.add.side_effect = wrapProv
        self.addCleanup(patcher.stop)

    def log(self, *args, **kwargs):
        from niprov.logging import log
        return log(*args, dependencies=self.dependencies, opts=self.opts, 
            **kwargs)

    def test_Returns_img(self):
        parents = ['/p/f1']
        new = '/p/f2'
        trans = 'Something cool'
        out = self.log(new, trans, parents)
        self.assertEqual(out, self.newimg)

    def test_Copies_fields_from_known_parent(self):
        self.locationFactory.completeString.side_effect = lambda p: p
        parent = '/p/f1'
        parents = [parent]
        parentProv = {'acquired':dt.now(),'subject':'JB','protocol':'T3'}
        parentImg = Mock()
        parentImg.provenance = parentProv
        self.repo.byLocation.side_effect = lambda x: {parent:parentImg}[x]
        self.log('new', 'trans', parents)
        self.assertEqual(self.provenancesCreated[0]['acquired'], parentProv['acquired'])
        self.assertEqual(self.provenancesCreated[0]['subject'], parentProv['subject'])
        self.assertEqual(self.provenancesCreated[0]['protocol'], parentProv['protocol'])

    def test_Adds_code_or_logtext(self):
        self.log('new', 'trans', 'old', code='abc', logtext='def')
        self.assertEqual(self.provenancesCreated[0]['code'],'abc')
        self.assertEqual(self.provenancesCreated[0]['logtext'],'def')

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

    def test_Doesnt_complain_if_parent_is_missing_basic_fields(self):
        img = Mock()
        img.provenance = {'acquired':dt.now()} #missing subject
        self.repo.byLocation.return_value = img
        provenance = self.log('new', 'trans', ['/p/f1parent'])
        self.assertNotIn('subject', self.provenancesCreated[0])

    def test_Calls_reconfigureOrGetConfiguration_on_dependencies(self):
        outOpts = Mock()
        outOpts.dryrun = True
        self.dependencies.reconfigureOrGetConfiguration.return_value = outOpts
        provenance = self.log(['/p/f1'], 'bla', ['/p/f2'], transient=True)
        self.dependencies.reconfigureOrGetConfiguration.assert_called_with(
            self.opts)

    def test_Can_pass_multiple_new_files(self):
        parents = ['p1','p2']
        new = ['/p/f2','/p/f3']
        trans = 'Something cool'
        self.locationFactory.completeString.side_effect = lambda p: 'l:'+p
        self.log(new, trans, parents)
        self.assertEqual(self.provenancesCreated[0]['parents'], ['l:p1','l:p2'])
        self.assertEqual(self.provenancesCreated[1]['parents'], ['l:p1','l:p2'])

    def test_Notifies_listener_and_exits_if_parent_unknown(self):
        self.repo.knowsByLocation.return_value = False
        parent = '/p/f1'
        parents = [parent]
        provenance = self.log('new', 'trans', parents)
        self.listener.unknownFile.assert_called_with(parent)
        assert not self.add.called

    def test_Finds_parent_provenance_using_completedString(self):
        self.locationFactory.completeString.side_effect = lambda p: 'l:'+p
        parent = '/p/f1'
        parents = [parent]
        provenance = self.log('new', 'trans', parents)
        self.repo.knowsByLocation.assert_called_with(self.provenancesCreated[0]['parents'][0])
        self.repo.byLocation.assert_called_with(self.provenancesCreated[0]['parents'][0])
        

