from mock import Mock, patch
from datetime import datetime as dt
from tests.ditest import DependencyInjectionTestBase


class LoggingTests(DependencyInjectionTestBase):

    def setUp(self):
        super(LoggingTests, self).setUp()
        self.repo.knowsByLocation.return_value = True
        self.opts = Mock()
        self.opts.dryrun = False
        img = Mock()
        img.provenance = {'acquired':dt.now(),
            'subject':'JD', 
            'protocol':'X',
            'technique':'abc',
            'repetition-time':1.0,
            'epi-factor':1.0,
            'magnetization-transfer-contrast':True,
            'diffusion':True,
            'echo-time':123,
            'flip-angle':892,
            'inversion-time':123}
        self.locationFactory.completeString.side_effect = lambda p: p
        self.repo.byLocation.return_value = img
        self.provenancesAdded = []
        def wrapProv(location, transient=False, provenance=False, dependencies=None):
            self.provenancesAdded.append(provenance)
            self.newimg = Mock()
            self.newimg.provenance = {'acquired':location}
            return (self.newimg, 'test')
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
        parentProv = {'acquired':dt.now(),
            'subject':'JD', 
            'protocol':'X',
            'technique':'abc',
            'repetition-time':1.0,
            'epi-factor':1.0,
            'magnetization-transfer-contrast':True,
            'diffusion':True,
            'echo-time':123,
            'flip-angle':892,
            'inversion-time':123}
        parentImg = Mock()
        parentImg.provenance = parentProv
        self.repo.byLocation.side_effect = lambda x: {parent:parentImg}[x]
        self.log('new', 'trans', parents)
        self.assertEqual(self.provenancesAdded[0]['acquired'], parentProv['acquired'])
        self.assertEqual(self.provenancesAdded[0]['subject'], parentProv['subject'])
        self.assertEqual(self.provenancesAdded[0]['protocol'], parentProv['protocol'])
        self.assertEqual(self.provenancesAdded[0]['technique'], parentProv['technique'])
        self.assertEqual(self.provenancesAdded[0]['repetition-time'], parentProv['repetition-time'])
        self.assertEqual(self.provenancesAdded[0]['epi-factor'], parentProv['epi-factor'])
        self.assertEqual(self.provenancesAdded[0]['magnetization-transfer-contrast'], 
            parentProv['magnetization-transfer-contrast'])
        self.assertEqual(self.provenancesAdded[0]['diffusion'], parentProv['diffusion'])
        self.assertEqual(self.provenancesAdded[0]['echo-time'], parentProv['echo-time'])
        self.assertEqual(self.provenancesAdded[0]['flip-angle'], parentProv['flip-angle'])
        self.assertEqual(self.provenancesAdded[0]['inversion-time'], parentProv['inversion-time'])

    def test_Adds_code_or_logtext(self):
        self.log('new', 'trans', 'old', code='abc', logtext='def')
        self.assertEqual(self.provenancesAdded[0]['code'],'abc')
        self.assertEqual(self.provenancesAdded[0]['logtext'],'def')

    def test_Determines_user_and_logs_them(self):
        self.users.determineUser.return_value = 'paprika'
        self.log('new', 'trans', 'old', user='mononoko')
        self.users.determineUser.assert_called_with('mononoko')
        self.assertEqual(self.provenancesAdded[0]['user'],'paprika')

    def test_Script_added_to_provenance(self):
        parents = ['/p/f1']
        new = '/p/f2'
        trans = 'Something cool'
        script = '/p/test.py'
        self.log(new, trans, parents, script=script)
        self.assertEqual(self.provenancesAdded[0]['script'], script)

    def test_Accepts_and_processes_custom_provenance(self):
        parents = ['/p/f1']
        new = '/p/f2'
        trans = 'Something cool'
        p = {'akey':'avalue'}
        self.log(new, trans, parents, provenance=p)
        self.assertEqual(self.provenancesAdded[0]['akey'], 'avalue')

    def test_Doesnt_complain_if_parent_is_missing_basic_fields(self):
        img = Mock()
        img.provenance = {'acquired':dt.now()} #missing subject
        self.repo.byLocation.return_value = img
        provenance = self.log('new', 'trans', ['/p/f1parent'])
        self.assertNotIn('subject', self.provenancesAdded[0])

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
        self.assertEqual(self.provenancesAdded[0]['parents'], ['l:p1','l:p2'])
        self.assertEqual(self.provenancesAdded[1]['parents'], ['l:p1','l:p2'])

    def test_Add_parent_if_parent_unknown(self):
        self.repo.knowsByLocation.return_value = False
        self.locationFactory.completeString.side_effect = lambda p: 'l:'+p
        provenance = self.log('new', 'trans', 'parentpath')
        self.add.assert_any_call('l:parentpath')
        self.listener.addUnknownParent.assert_called_with('l:parentpath')

    def test_Uses_validated_location_for_parent_lookup(self):
        self.locationFactory.completeString.side_effect = lambda p: 'l:'+p
        provenance = self.log('new', 'trans', 'parentpath')
        self.repo.knowsByLocation.assert_called_with('l:parentpath')
        self.repo.byLocation.assert_called_with('l:parentpath')

    def test_If_parent_unknown_uses_add_return_value(self):
        """In this case the parent provenance should be obtained from
        what add() returns.
        """
        self.repo.knowsByLocation.return_value = False
        parent = 'unknown/parent/path.f'
        provenance = self.log('new', 'trans', [parent])
        assert not self.repo.byLocation.called
        loggedFileProv = self.provenancesAdded[1] # [0]: parent [1]: newly logged
        ## add function is mocked to set 'acquired' field to location passed
        ## since acquired is an inheritable field, it should show up in kid:
        self.assertEqual(loggedFileProv['acquired'], 'unknown/parent/path.f')
        

