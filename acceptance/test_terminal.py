import unittest, os, shutil, sys
from cStringIO import StringIO 
absp = os.path.abspath


class TerminalApiTests(unittest.TestCase):

    def setUp(self):
        self.dbpath = os.path.expanduser(os.path.join('~','provenance_test.json'))
        if os.path.exists(self.dbpath):
            os.remove(self.dbpath)
        os.mkdir('temp')
        from niprov import ProvenanceContext
        self.provenance = ProvenanceContext()
        self.provenance.config.database_type = 'file'
        self.provenance.config.database_url = self.dbpath
        self.provenance.config.verbose = False
        self.oldstdout = sys.stdout
        sys.stdout = self.stdout = StringIO()

    def tearDown(self):
        sys.stdout = self.oldstdout
        self.stdout.close()
        shutil.rmtree('temp')

    @unittest.skip("Doesn't work on travis")
    def test_Report_pipeline(self):
        self.provenance.discover('testdata')
        raw = os.path.abspath('testdata/eeg/stub.cnt')
        self.provenance.log(absp('p1a.f'), 'test', raw, transient=True)
        self.provenance.log(absp('p1b.f'), 'test', raw, transient=True)
        self.provenance.log(absp('p2.f'), 'test', absp('p1a.f'), transient=True)
        self.provenance.export(None, 'stdout', 'simple', pipeline=True)
        exp = ''
        exp += '+---stub.cnt\n'
        exp += '|   +---p1a.f\n'
        exp += '|   |   +---p2.f\n'
        #exp += '|   +---p1b.f\n' # p1b is not related to p2f
        import time
        time.sleep(0.3)
        self.assertIn(exp, self.stdout.getvalue())


if __name__ == '__main__':
    unittest.main()

