import unittest
from mock import Mock

class ReportingTests(unittest.TestCase):

    def test_Loads_file_with_nibabel(self):
        import niprov
        log = Mock()
        repo = Mock()
        out = niprov.report(repository=repo)
        self.assertEqual(out, repo.all())


