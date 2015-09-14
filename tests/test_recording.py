from __future__ import print_function
import unittest
from mock import Mock



class RecordingTests(unittest.TestCase):

    def setUp(self):
        import niprov.recording as recording
        self.log = Mock()
        self.opts = Mock()
        self.opts.dryrun = False
        self.sub = Mock()
        self.listener = Mock()
        recording.log = self.log
        self.recording = recording
        self.dependencies = Mock()
        self.dependencies.reconfigureOrGetConfiguration.return_value = self.opts
        self.dependencies.getExternals.return_value = self.sub
        self.dependencies.getListener.return_value = self.listener

    def record(self, cmd, **kwargs):
        self.recording.record(cmd, dependencies=self.dependencies, 
            opts=self.opts, **kwargs)

    def test_Executes_commands(self):
        cmd = ['mytransform','-out','newfile.f','-in','oldfile.f']
        self.record(cmd)
        self.sub.run.assert_any_call(cmd)

    def test_Extracts_provenance_from_commands(self):
        cmd = ['mytransform','-out','newfile.f','-in','oldfile.f']
        self.record(cmd)
        self.log.assert_called_with(['newfile.f'],'mytransform',['oldfile.f'], 
            transient=False, code=' '.join(cmd), logtext=self.sub.run().output, 
            script=None, opts=self.opts, provenance={})

    def test_If_parent_or_new_provided_override_parsed(self):
        cmd = ['mytransform','-out','newfile.f','-in','oldfile.f']
        self.record(cmd, parents=['customParent'], new='customNew')
        self.log.assert_called_with(['customNew'],'mytransform',['customParent'],
            transient=False, code=' '.join(cmd), logtext=self.sub.run().output, 
            script=None, opts=self.opts, provenance={})

    def test_Passes_transient_flag(self):
        cmd = ['mytransform','-out','newfile.f','-in','oldfile.f']
        self.record(cmd, transient=True)
        self.log.assert_called_with(['newfile.f'],'mytransform',['oldfile.f'], 
            transient=True, code=' '.join(cmd), logtext=self.sub.run().output, 
            script=None, opts=self.opts, provenance={})

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
            script=None, opts=self.opts, provenance={})

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
            opts=self.opts, provenance={'args':args, 'kwargs':kwargs})

    def test_Python_code_output_captured(self):
        def myfunc():
            print('Hello MyFunc')
        args = []
        kwargs = {}
        self.record(myfunc, args=args, kwargs=kwargs, new='new.f', parents=['old.f'])
        self.log.assert_called_with(['new.f'],myfunc.func_name,['old.f'], 
            transient=False, code=None, logtext='Hello MyFunc\n', 
            script=myfunc.func_code.co_filename,
            opts=self.opts, provenance={'args':args, 'kwargs':kwargs})

    def test_On_dryrun_doesnt_execute_python_code(self):
        myfunc = Mock()
        myfunc.side_effect = lambda a,b,one=None,two=None: None
        myfunc.func_name = 'myfunc'
        args = ['foo','bar']
        kwargs = {'one':'foz','two':'baz'}
        self.opts.dryrun = True
        self.record(myfunc, args=args, kwargs=kwargs)
        assert not myfunc.called, "Passed function was called on dry run."

    def test_On_dryrun_doesnt_execute_commands(self):
        self.opts.dryrun = True
        cmd = ['mytransform','-out','newfile.f','-in','oldfile.f']
        self.record(cmd)
        assert not self.sub.run.called, "Command was executed on dry run."

    def test_Passes_opts_to_log(self):
        cmd = ['mytransform','-out','newfile.f','-in','oldfile.f']
        self.record(cmd, transient=True)
        self.log.assert_called_with(['newfile.f'],'mytransform',['oldfile.f'], 
            transient=True, code=' '.join(cmd), logtext=self.sub.run().output, 
            script=None, provenance={}, opts=self.opts)

    def test_Abbreviated_versions_of_out_and_in(self):
        cmd = ['mytransform','-o','newfile.f','-i','oldfile.f']
        self.record(cmd)
        self.log.assert_called_with(['newfile.f'],'mytransform',['oldfile.f'], 
            transient=False, code=' '.join(cmd), logtext=self.sub.run().output, 
            script=None, opts=self.opts, provenance={})

    def test_Passes_listener_bash_command(self):
        def myfunc():
            print('Hello MyFunc')
        args = []
        kwargs = {}
        self.record(myfunc, args=args, kwargs=kwargs, new='new.f', parents=['old.f'])
        assert not self.listener.receivedBashCommand.called
        cmd = ['mytransform','-o','newfile.f','-i','oldfile.f']
        self.record(cmd)
        self.listener.receivedBashCommand.assert_called_with(cmd)

    def test_Calls_reconfigureOrGetConfiguration_on_dependencies(self):
        cmd = ['mytransform','-out','newfile.f','-in','oldfile.f']
        outOpts = Mock()
        outOpts.dryrun = True
        self.dependencies.reconfigureOrGetConfiguration.return_value = outOpts
        self.record(cmd, transient=True)
        self.dependencies.reconfigureOrGetConfiguration.assert_called_with(
            self.opts)
        assert not self.sub.run.called

