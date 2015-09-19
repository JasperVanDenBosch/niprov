import unittest
from mock import Mock
from tests.ditest import DependencyInjectionTestBase


class ApprovalTests(DependencyInjectionTestBase):

    def setUp(self):
        super(ApprovalTests, self).setUp()

    def test_markForApproval_tells_repo_to_set_approval_to_pending(self):
        import niprov
        niprov.markForApproval(['f1','f2'], dependencies=self.dependencies)
        self.repo.updateApproval.assert_any_call('f1','pending')
        self.repo.updateApproval.assert_any_call('f2','pending')

    def test_Approve_tells_repo_to_set_approval_to_granted(self):
        import niprov
        niprov.approve('fx12', dependencies=self.dependencies)
        self.repo.updateApproval.assert_any_call('fx12','granted')

    def test_markedForApproval_lists_files_marked(self):
        import niprov
        markedFiles = niprov.markedForApproval(dependencies=self.dependencies)
        self.repo.byApproval.assert_called_with('pending')
        self.assertEqual(self.repo.byApproval(), markedFiles)

    def test_markedForApproval_tells_listener_about_files(self):
        import niprov
        markedFiles = niprov.markedForApproval(dependencies=self.dependencies)
        self.listener.filesMarkedForApproval.assert_called_with(
            markedFiles)

    def test_selectApproved(self):
        import niprov
        self.locationFactory.completeString.side_effect = lambda p: p
        a1 = self.mockImg()
        a1.provenance['approval'] = 'granted'
        a2 = self.mockImg()
        a2.provenance['approval'] = 'granted'
        b1 = self.mockImg()
        c1 = self.mockImg()
        c1.provenance['approval'] = 'pending'
        self.repo.byLocation.side_effect = lambda p: {'a1':a1,'b1':b1,'a2':a2,'c1':c1}[p]
        selected = niprov.selectApproved(['a1','b1','a2','c1'], 
            dependencies=self.dependencies)
        self.locationFactory.completeString.assert_any_call('a1')
        self.locationFactory.completeString.assert_any_call('b1')
        self.locationFactory.completeString.assert_any_call('a2')
        self.locationFactory.completeString.assert_any_call('c1')
        self.assertEqual(selected, [a1.path, a2.path])

    def mockImg(self):
        img = Mock()
        img.provenance = {}
        return img

