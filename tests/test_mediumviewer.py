#!/usr/bin/python
# -*- coding: UTF-8 -*-
from mock import Mock, sentinel, patch
from tests.ditest import DependencyInjectionTestBase


class ViewerMediumTests(DependencyInjectionTestBase):

    def test_Returns_input(self):
        from niprov.mediumviewer import ViewerMedium
        exporter = ViewerMedium()
        fmt = Mock()
        with patch('niprov.mediumviewer.webbrowser') as webbrowser:
            exporter.export('the filename', fmt)
            webbrowser.open.assert_called_with('the filename')



