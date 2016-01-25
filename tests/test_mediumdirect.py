#!/usr/bin/python
# -*- coding: UTF-8 -*-
from mock import Mock, sentinel
from tests.ditest import DependencyInjectionTestBase


class DirectMediumTests(DependencyInjectionTestBase):

    def test_Returns_input(self):
        from niprov.mediumdirect import DirectMedium
        exporter = DirectMedium()
        fmt = Mock()
        self.assertEqual(sentinel.one, exporter.export(sentinel.one, fmt))



