import unittest
from mock import Mock


class RecordingTests(unittest.TestCase):

    def test_Executes_commands(self):
        import niprov.recording as recording
        log = Mock()
        recording.log = log
        cmd = ['mytransform','-out','newfile.f','-in','oldfile.f']
        sub = Mock()
        recording.record(cmd, externals=sub)
        sub.run.assert_any_call(cmd)

    def test_Extracts_provenance_from_commands(self):
        import niprov.recording as recording
        log = Mock()
        cmd = ['mytransform','-out','newfile.f','-in','oldfile.f']
        sub = Mock()
        recording.log = log
        recording.record(cmd, externals=sub)
        log.assert_called_with('newfile.f','mytransform','oldfile.f',
            code=' '.join(cmd), logtext=sub.run().output)

    def test_If_parent_or_new_provided_override_parsed(self):
        import niprov.recording as recording
        log = Mock()
        cmd = ['mytransform','-out','newfile.f','-in','oldfile.f']
        sub = Mock()
        recording.log = log
        recording.record(cmd, parent='customParent', new='customNew',
            externals=sub)
        log.assert_called_with('customNew','mytransform','customParent',
            code=' '.join(cmd), logtext=sub.run().output)
        

