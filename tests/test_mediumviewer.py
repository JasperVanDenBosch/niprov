#!/usr/bin/python
# -*- coding: UTF-8 -*-
from mock import Mock, sentinel, patch
from tests.ditest import DependencyInjectionTestBase


class ViewerMediumTests(DependencyInjectionTestBase):

    def test_Returns_input(self):
        from niprov.mediumviewer import ViewerMedium
        exporter = ViewerMedium(sentinel.dependencies)
        with patch('niprov.mediumviewer.webbrowser') as webbrowser:
            exporter.export('the filename', sentinel.format)
            webbrowser.open.assert_called_with('the filename')

    def test_Does_nothing_if_passed_None(self):
        from niprov.mediumviewer import ViewerMedium
        exporter = ViewerMedium(sentinel.dependencies)
        with patch('niprov.mediumviewer.webbrowser') as webbrowser:
            exporter.export(None, sentinel.format)
            assert not webbrowser.open.called

    def test_Can_be_called_without_format(self):
        from niprov.mediumviewer import ViewerMedium
        exporter = ViewerMedium(sentinel.dependencies)
        with patch('niprov.mediumviewer.webbrowser') as webbrowser:
            exporter.export(None)



