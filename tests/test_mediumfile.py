#!/usr/bin/python
# -*- coding: UTF-8 -*-
from mock import Mock, sentinel, patch
from tests.ditest import DependencyInjectionTestBase


class FileMediumTests(DependencyInjectionTestBase):

    def test_Writes_formattedProvenance_to_file(self):
        from niprov.mediumfile import FileMedium
        medium = FileMedium(self.dependencies)
        out = medium.export('Once upon a time..')
        self.assertEqual('Once upon a time..', 
            self.filesys.write.call_args[0][1])

    def test_Comes_up_with_filename(self):
        from niprov.mediumfile import FileMedium
        self.clock.getNowString.return_value = 'hammertime'
        medium = FileMedium(self.dependencies)
        out = medium.export('provstr')
        self.filesys.write.assert_called_with('provenance_hammertime.txt',
            'provstr')

    def test_Returns_filename(self):
        from niprov.mediumfile import FileMedium
        self.clock.getNowString.return_value = 'hammertime'
        medium = FileMedium(self.dependencies)
        out = medium.export('provstr')
        self.assertEqual('provenance_hammertime.txt', out)




