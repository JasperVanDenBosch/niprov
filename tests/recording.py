from __future__ import print_function
import unittest
from mock import Mock



class RecordingTests(unittest.TestCase):

    def setUp(self):
        import niprov.recording as recording
        self.log = Mock()
        self.sub = Mock()
        self.listener = Mock()
        recording.log = self.log
        self.recording = recording

    def record(self, cmd, **kwargs):
        self.recording.record(cmd, externals=self.sub, listener=self.listener, **kwargs)

    def test_Executes_commands(self):
        cmd = ['mytransform','-out','newfile.f','-in','oldfile.f']
        self.record(cmd)
        self.sub.run.assert_any_call(cmd)

    def test_Extracts_provenance_from_commands(self):
        cmd = ['mytransform','-out','newfile.f','-in','oldfile.f']
        self.record(cmd)
        self.log.assert_called_with(['newfile.f'],'mytransform',['oldfile.f'], 
            transient=False, code=' '.join(cmd), logtext=self.sub.run().output, 
            script=None, provenance={})

    def test_If_parent_or_new_provided_override_parsed(self):
        cmd = ['mytransform','-out','newfile.f','-in','oldfile.f']
        self.record(cmd, parents=['customParent'], new='customNew')
        self.log.assert_called_with(['customNew'],'mytransform',['customParent'],
            transient=False, code=' '.join(cmd), logtext=self.sub.run().output, 
            script=None, provenance={})

    def test_Passes_transient_flag(self):
        cmd = ['mytransform','-out','newfile.f','-in','oldfile.f']
        self.record(cmd, transient=True)
        self.log.assert_called_with(['newfile.f'],'mytransform',['oldfile.f'], 
            transient=True, code=' '.join(cmd), logtext=self.sub.run().output, 
            script=None, provenance={})

    def test_Informs_listener_about_interpretation(self):
        cmd = ['mytransform','-out','newfile.f','-in','oldfile.f']
        self.record(cmd)
        self.listener.interpretedRecording.assert_called_with(
            ['newfile.f'],'mytransform',['oldfile.f'])

    def test_Works_on_single_string_too(self):
        cmd = 'mytransform -out newfile.f -in oldfile.f'
        self.record(cmd)
        self.sub.run.assert_called_with(cmd.split())
        self.log.assert_called_with(['newfile.f'],'mytransform',['oldfile.f'], 
            transient=False, code=cmd, logtext=self.sub.run().output, 
            script=None, provenance={})

    def test_Python_code(self):
        myfunc = Mock()
        myfunc.side_effect = lambda a,b,one=None,two=None: None
        myfunc.func_name = 'myfunc'
        args = ['foo','bar']
        kwargs = {'one':'foz','two':'baz'}
        self.record(myfunc, args=args, kwargs=kwargs, new='new.f', parents=['old.f'])
        myfunc.assert_called_with(*args, **kwargs)
        self.log.assert_called_with(['new.f'],myfunc.func_name,['old.f'], 
            transient=False, code=None, logtext='', 
            script=myfunc.func_code.co_filename,
            provenance={'args':args, 'kwargs':kwargs})

    def test_Python_code_output_captured(self):
        def myfunc():
            print('Hello MyFunc')
        args = []
        kwargs = {}
        self.record(myfunc, args=args, kwargs=kwargs, new='new.f', parents=['old.f'])
        self.log.assert_called_with(['new.f'],myfunc.func_name,['old.f'], 
            transient=False, code=None, logtext='Hello MyFunc\n', 
            script=myfunc.func_code.co_filename,
            provenance={'args':args, 'kwargs':kwargs})


        

