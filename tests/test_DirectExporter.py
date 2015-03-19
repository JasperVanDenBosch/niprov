#!/usr/bin/python
# -*- coding: UTF-8 -*-
from unittest import TestCase
from mock import Mock, sentinel


class DirectExporterTests(TestCase):

    def test_Returns_input(self):
        from niprov.directexporter import DirectExporter
        exporter = DirectExporter()
        self.assertEqual(sentinel.one, exporter.exportSingle(sentinel.one))
        self.assertEqual(sentinel.list, exporter.exportList(sentinel.list))

    def test_For_narrative_form_Returns_narrator_output(self):
        from niprov.directexporter import DirectExporter
        narrator = Mock()
        exporter = DirectExporter(form='narrative',narrator=narrator)
        out = exporter.exportNarrative(sentinel.one)
        narrator.narrate.assert_called_with(sentinel.one)
        self.assertEqual(out, narrator.narrate(sentinel.one))

