import unittest, os
from mock import Mock, patch, call, sentinel
from tests.ditest import DependencyInjectionTestBase


class AddTests(DependencyInjectionTestBase):

    def setUp(self):
        super(AddTests, self).setUp()
        self.config.dryrun = False
        self.repo.byLocation.return_value = None
        self.query.copiesOf.return_value = []
        self.img = Mock()
        self.lastProvenance = None
        def locAt(loc, provenance):
            self.lastProvenance = provenance
            self.lastPath = loc
            return self.img
        self.fileFactory.locatedAt.side_effect = locAt
        patcher = patch('niprov.adding.datetime')
        self.datetime = patcher.start()
        self.addCleanup(patcher.stop)

    def add(self, path, **kwargs):
        from niprov.adding import add
        with patch('niprov.adding.inheritFrom') as self.inheritFrom:
            return add(path, dependencies=self.dependencies, **kwargs)

    def assertNotCalledWith(self, m, *args, **kwargs):
        c = call(*args, **kwargs)
        assert c not in m.call_args_list, "Unexpectedly found call: "+str(c)

    def test_Returns_provenance_and_informs_listener(self):
        new = '/p/f2'
        image = self.add(new)
        self.listener.fileAdded.assert_called_with(self.img)
        self.assertEqual(image, self.img)

    def test_Sets_transient_flag_if_provided(self):
        image = self.add('/p/f1', transient=True)
        self.assertEqual(self.lastProvenance['transient'],True)

    def test_Creates_ImageFile_object_with_factory(self):
        image = self.add('p/afile.f')
        self.assertIs(self.img, image)

    def test_Calls_inspect(self):
        image = self.add('p/afile.f')
        self.img.inspect.assert_called_with()

    def test_If_inspect_raises_exceptions_tells_listener_and_doesnt_save(self):
        self.img.inspect.side_effect = IOError
        image = self.add('p/afile.f')
        assert not self.repo.add.called
        assert not self.repo.update.called
        self.listener.fileError.assert_called_with(self.img.path)
        self.assertEqual(self.img.status, 'failed')

    def test_If_dryrun_doesnt_talk_to_repo_and_status_is_test(self):
        self.config.dryrun = True
        image = self.add('p/afile.f')
        assert not self.repo.add.called
        assert not self.repo.update.called
        assert not self.img.inspect.called

    def test_accepts_optional_provenance(self):
        image = self.add('p/afile.f', provenance={'fob':'bez'})
        self.assertEqual(self.lastProvenance['fob'],'bez')

    def test_If_file_doesnt_exists_raises_error(self):
        self.filesys.fileExists.return_value = False
        self.assertRaises(IOError, self.add, self.img.location.path)
        self.filesys.fileExists.assert_called_with(self.img.location.path)

    def test_For_nonexisting_transient_file_behaves_normal(self):
        self.filesys.fileExists.return_value = False
        self.add('p/afile.f', transient=True)

    def test_Doesnt_inspect_transient_files(self):
        self.add('p/afile.f', transient=True)
        assert not self.img.inspect.called

    def test_Adds_timestamp(self):
        image = self.add('p/afile.f')
        self.assertEqual(self.lastProvenance['added'],self.datetime.now())

    def test_Adds_uid(self):
        with patch('niprov.adding.shortuuid') as shortuuid:
            shortuuid.uuid.return_value = 'abcdefghijklmn'
            image = self.add('p/afile.f')
            self.assertEqual(self.lastProvenance['id'],'abcdef')

    def test_If_config_attach_set_calls_attach_on_file(self):
        self.config.attach = False
        self.add('p/afile.f')
        assert not self.img.attach.called, "Shouldnt attach if not configured."
        self.config.attach = True
        self.config.attach_format = 'abracadabra'
        self.add('p/afile.f', transient=True)
        assert not self.img.attach.called, "Shouldnt attach to transient file."
        self.add('p/afile.f')
        self.img.attach.assert_called_with('abracadabra')

    def test_If_file_unknown_adds_it(self):                             # A
        self.repo.byLocation.return_value = None
        self.repo.getSeries.return_value = None
        image = self.add('p/afile.f')
        self.repo.add.assert_any_call(self.img)

    def test_If_file_is_version_but_not_series(self):                    # B
        previousVersion = Mock()
        self.repo.byLocation.return_value = previousVersion
        self.repo.getSeries.return_value = None
        img = self.add('p/afile.f')
        self.img.keepVersionsFromPrevious.assert_called_with(previousVersion)
        self.repo.update.assert_any_call(self.img)

    def test_If_file_is_version_and_series(self):                        # C
        previousVersion = Mock()
        series = Mock()
        self.repo.byLocation.return_value = previousVersion
        self.repo.getSeries.return_value = series
        image = self.add('p/afile.f')
        self.img.keepVersionsFromPrevious.assert_called_with(previousVersion)
        self.repo.update.assert_any_call(self.img)

    def test_If_file_not_version_but_series_and_not_in_there_yet(self):   # D1
        series = Mock()
        series.hasFile.return_value = False
        series.mergeWith.return_value = series
        self.repo.byLocation.return_value = None
        self.repo.getSeries.return_value = series
        image = self.add('p/afile.f')
        series.mergeWith.assert_called_with(self.img)
        self.repo.update.assert_any_call(series)

    def test_If_file_not_version_but_series_has_file(self):               # D2
        series = Mock()
        series.hasFile.return_value = True
        self.repo.byLocation.return_value = None
        self.repo.getSeries.return_value = series
        image = self.add('p/afile.f')
        assert not series.mergeWith.called
        self.img.keepVersionsFromPrevious.assert_called_with(series)
        self.repo.update.assert_any_call(self.img)

    def test_copiesOf_not_called_before_inspect(self):
        def testIfInspectedAndReturnEptyList(img):
            img.inspect.assert_called_with()
            return []
        self.query.copiesOf.side_effect = testIfInspectedAndReturnEptyList
        image = self.add('p/afile.f')

    def test_getSeries_not_called_before_inspect(self):
        self.repo.getSeries.side_effect = lambda img: img.inspect.assert_called_with()
        image = self.add('p/afile.f')

    def test_copiesOf_not_called_if_parent_available(self):
        image = self.add('p/afile.f', provenance={'parents':[sentinel.parent]})
        assert not self.query.copiesOf.called

    def test_Found_copy_set_as_parent_inherits_and_flags_and_informs_listener(self):
        self.img.provenance = {}
        copy = Mock()
        copy.provenance = {'location':'copy-location'}
        self.query.copiesOf.return_value = [self.img, copy]
        out = self.add('p/afile.f')
        self.inheritFrom.assert_called_with(self.img.provenance, copy.provenance)
        self.listener.usingCopyAsParent.assert_called_with(copy)
        self.assertEqual(copy.location.toString(), out.provenance['parents'][0])
        self.assertEqual(True, out.provenance['copy-as-parent'])

    def test_If_only_copy_is_same_location_ignores_it(self):
        self.img.provenance = {}
        self.query.copiesOf.return_value = [self.img]
        out = self.add('p/afile.f')
        assert not self.inheritFrom.called
        assert not self.listener.usingCopyAsParent.called
        self.assertNotIn('parents', out.provenance)
        self.assertNotIn('copy-as-parent', out.provenance)

        

