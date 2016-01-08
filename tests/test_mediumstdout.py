#!/usr/bin/python
# -*- coding: UTF-8 -*-
from mock import Mock, sentinel, patch
from tests.ditest import DependencyInjectionTestBase


class StdoutMediumTests(DependencyInjectionTestBase):

    def test_Prints_formatted_provenance(self):
        from niprov.mediumstdout import StandardOutputMedium
        mprint = Mock()
        with patch('__builtin__.print') as mprint:
            exporter = StandardOutputMedium()
            out = exporter.export('Goodbye World!')
            mprint.assert_called_with('Goodbye World!')



