import unittest
from mock import Mock


class ApprovalTests(unittest.TestCase):

    def setUp(self):
        self.repo = Mock()

    def test_markForApproval_tells_repo_to_set_approval_to_pending(self):
        import niprov
        niprov.markForApproval(['f1','f2'], repository=self.repo)
        self.repo.updateApproval.assert_any_call('f1','pending')
        self.repo.updateApproval.assert_any_call('f2','pending')

    def test_Approve_tells_repo_to_set_approval_to_granted(self):
        import niprov
        niprov.approve('fx12', repository=self.repo)
        self.repo.updateApproval.assert_any_call('fx12','granted')

    def test_markedForApproval_lists_files_marked(self):
        import niprov
        markedFiles = niprov.markedForApproval(repository=self.repo)
        self.repo.byApproval.assert_called_with('pending')
        self.assertEqual(self.repo.byApproval(), markedFiles)
        
#        marked = niprov.markedForApproval()
#        for f in ['f1','f2','f3','f4']:
#            self.assertIn(f, marked)
#        self.assertNotIn('f5', marked)


