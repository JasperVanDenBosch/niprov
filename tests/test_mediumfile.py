#!/usr/bin/python
# -*- coding: UTF-8 -*-
from mock import Mock, sentinel, patch
from tests.ditest import DependencyInjectionTestBase


class FileMediumTests(DependencyInjectionTestBase):

    def test_Writes_formattedProvenance_to_file(self):
        from niprov.mediumfile import FileMedium
        medium = FileMedium(self.dependencies)
        out = medium.export('Once upon a time..', self.format)
        self.assertEqual('Once upon a time..', 
            self.filesys.write.call_args[0][1])

    def test_Comes_up_with_filename(self):
        from niprov.mediumfile import FileMedium
        self.clock.getNowString.return_value = 'hammertime'
        medium = FileMedium(self.dependencies)
        out = medium.export('provstr', self.format)
        self.filesys.write.assert_called_with('provenance_hammertime.txt',
            'provstr')

    def test_Returns_filename(self):
        from niprov.mediumfile import FileMedium
        self.clock.getNowString.return_value = 'hammertime'
        medium = FileMedium(self.dependencies)
        out = medium.export('provstr', self.format)
        self.assertEqual('provenance_hammertime.txt', out)

    def test_Reports_filename_to_listener(self):
        from niprov.mediumfile import FileMedium
        self.clock.getNowString.return_value = 'hammertime'
        medium = FileMedium(self.dependencies)
        out = medium.export('provstr', self.format)
        self.listener.exportedToFile.assert_called_with(
            'provenance_hammertime.txt')

    def test_Specific_extension_for_format(self):
        from niprov.mediumfile import FileMedium
        self.clock.getNowString.return_value = 'hammertime'
        medium = FileMedium(self.dependencies)
        fmt = Mock()
        fmt.fileExtension = 'prv'
        out = medium.export('provstr', fmt)
        self.listener.exportedToFile.assert_called_with(
            'provenance_hammertime.prv')


    def test_For_PictureCache_format_simply_provides_filename(self):
        from niprov.mediumfile import FileMedium
        from niprov.pictures import PictureCache
        medium = FileMedium(self.dependencies)
        fmt = PictureCache(Mock())
        out = medium.export('provstr', fmt)
        self.listener.exportedToFile.assert_called_with('provstr')
        self.assertEqual(out, 'provstr')



