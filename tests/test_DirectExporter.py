#!/usr/bin/python
# -*- coding: UTF-8 -*-
from unittest import TestCase
from mock import sentinel


class DirectExporterTests(TestCase):

    def test_Returns_input(self):
        from niprov.directexporter import DirectExporter
        exporter = DirectExporter()
        self.assertEqual(sentinel.one, exporter.export(sentinel.one))
        self.assertEqual(sentinel.list, exporter.exportList(sentinel.list))
