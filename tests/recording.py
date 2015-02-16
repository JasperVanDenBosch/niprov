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
        log.assert_called_with('newfile.f','mytransform',['oldfile.f'], 
            transient=False, code=' '.join(cmd), logtext=sub.run().output)

    def test_If_parent_or_new_provided_override_parsed(self):
        import niprov.recording as recording
        log = Mock()
        cmd = ['mytransform','-out','newfile.f','-in','oldfile.f']
        sub = Mock()
        recording.log = log
        recording.record(cmd, parents=['customParent'], new='customNew',
            externals=sub)
        log.assert_called_with('customNew','mytransform',['customParent'],
            transient=False, code=' '.join(cmd), logtext=sub.run().output)

    def test_Passes_transient_flag(self):
        import niprov.recording as recording
        log = Mock()
        cmd = ['mytransform','-out','newfile.f','-in','oldfile.f']
        sub = Mock()
        recording.log = log
        recording.record(cmd, transient=True, externals=sub)
        log.assert_called_with('newfile.f','mytransform',['oldfile.f'], 
            transient=True, code=' '.join(cmd), logtext=sub.run().output)
        

