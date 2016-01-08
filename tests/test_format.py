from mock import Mock, sentinel
from tests.ditest import DependencyInjectionTestBase


class FormatTests(DependencyInjectionTestBase):

    def test_If_export_called_with_list_calls_exportList(self):
        from niprov.format import Format
        exp = Format()
        exp.exportList = Mock()
        out = exp.export([sentinel.p1, sentinel.p2])
        exp.exportList.assert_called_with([sentinel.p1, sentinel.p2])
        self.assertEqual(out, exp.exportList())

    def test_If_export_called_with_list_calls_exportSingle(self):
        from niprov.format import Format
        exp = Format()
        exp.exportSingle = Mock()
        out = exp.export(sentinel.p1)
        exp.exportSingle.assert_called_with(sentinel.p1)
        self.assertEqual(out, exp.exportSingle())

    def test_If_created_with_narrative_calls_exportNarrative(self):
        from niprov.format import Format
        exp = Format(form='narrative')
        exp.exportNarrative = Mock()
        out = exp.export(sentinel.p1)
        exp.exportNarrative.assert_called_with(sentinel.p1)
        self.assertEqual(out, exp.exportNarrative())

    def test_If_called_with_dict_calls_exportStatistics(self):
        from niprov.format import Format
        exp = Format()
        exp.exportStatistics = Mock()
        out = exp.export({'a':'b'})
        exp.exportStatistics.assert_called_with({'a':'b'})
        self.assertEqual(out, exp.exportStatistics())

    def test_If_created_with_pipeline_calls_exportPipeline(self):
        from niprov.format import Format
        from niprov.basefile import BaseFile
        exp = Format(form='pipeline', dependencies=self.dependencies)
        exp.exportPipeline = Mock()
        img = BaseFile('xyz.f')
        out = exp.export(img)
        self.pipelineFactory.forFile.assert_called_with(img)
        exp.exportPipeline.assert_called_with(self.pipelineFactory.forFile())
        self.assertEqual(out, exp.exportPipeline())

    def test_If_created_with_pipeline_but_called_with_list_raise_error(self):
        from niprov.format import Format
        exp = Format(form='pipeline', dependencies=self.dependencies)
        exp.exportPipeline = Mock()
        with self.assertRaisesRegexp(TypeError, 
                'Cannot export Pipeline for multiple files.'):
            out = exp.export([sentinel.p1, sentinel.p2])



