#!/usr/bin/python
# -*- coding: UTF-8 -*-
from unittest import TestCase
from mock import Mock, sentinel, patch


class StdoutExporterTests(TestCase):

    def test_For_narrative_form_Returns_narrator_output(self):
        mprint = Mock()
        dependencies = Mock()
        from niprov.stdout import StandardOutputExporter
        narrator = Mock()
        dependencies.getNarrator.return_value = narrator
        with patch('__builtin__.print') as mprint:
            exporter = StandardOutputExporter(form='narrative', 
                dependencies=dependencies)
            out = exporter.exportNarrative(sentinel.one)
            narrator.narrate.assert_called_with(sentinel.one)
            mprint.assert_any_call(narrator.narrate())

    def test_Statistics(self):
        mprint = Mock()
        dependencies = Mock()
        from niprov.stdout import StandardOutputExporter
        with patch('__builtin__.print') as mprint:
            exporter = StandardOutputExporter(dependencies=dependencies)
            exporter.exportStatistics({'count':123,'totalsize':678})
            mprint.assert_any_call(' Number of files: 123')
            mprint.assert_any_call(' Total file size: 678')
