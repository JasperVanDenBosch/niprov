import unittest
from mock import Mock


class RecordingTests(unittest.TestCase):

    def test_Executes_commands(self):
        from niprov.recording import record
        cmd = ['mytransform','-out','newfile.f','-in','oldfile.f']
        sub = Mock()
        record(cmd, externals=sub)
        sub.run.assert_any_call(cmd)

    def test_Extracts_transformation_and_new_file_and_ancestor(self):
        import niprov.recording as recording
        log = Mock()
        cmd = ['mytransform','-out','newfile.f','-in','oldfile.f']
        sub = Mock()
        recording.log = log
        recording.record(cmd, externals=sub)
        log.assert_called_with('mytransform','oldfile.f','newfile.f')

#    def test_Does_not_log_provenance_if_command_fails(self):
#        from niprov.recording import record
#        self.fail()


        

