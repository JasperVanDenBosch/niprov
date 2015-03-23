#!/usr/bin/python
# -*- coding: UTF-8 -*-
from unittest import TestCase
from mock import Mock, sentinel, patch


class StdoutExporterTests(TestCase):

    def test_For_narrative_form_Returns_narrator_output(self):
        mprint = Mock()
        from niprov.stdout import StandardOutputExporter
        narrator = Mock()
        with patch('__builtin__.print') as mprint:
            exporter = StandardOutputExporter(form='narrative', 
                narrator=narrator)
            out = exporter.exportNarrative(sentinel.one)
            narrator.narrate.assert_called_with(sentinel.one)
            mprint.assert_any_call(narrator.narrate())

