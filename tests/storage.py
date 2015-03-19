#!/usr/bin/python
# -*- coding: UTF-8 -*-
import unittest
from mock import Mock
from datetime import datetime
import json
import random
import copy


class StorageTests(unittest.TestCase):

    def setUp(self):
        r = random.randint(1000,9999)
        self.templocation = '/var/tmp/provenance-{0}.json'.format(r)
        self.fileFactory = Mock()

    def test_Can_add_file_and_retrieve_it(self):
        from niprov.jsonfile import JsonFile
        repo = JsonFile(factory=self.fileFactory)
        repo.datafile = self.templocation
        provenance = self.sampleProvenanceRecord()
        repo.add(provenance)
        repo2 = JsonFile(factory=self.fileFactory)
        repo2.datafile = self.templocation
        out = repo2.byPath(provenance['path'])
        self.fileFactory.fromProvenance.assert_called_with(provenance)
        self.assertEqual(out, self.fileFactory.fromProvenance())

    def test_If_file_doesnt_exist_all_returns_empty_list(self):
        from niprov.jsonfile import JsonFile
        filesys = Mock()
        filesys.read.side_effect = IOError(
            "[Errno 2] No such file or directory: 'provenance.json'")
        repo = JsonFile(filesys)
        repo.datafile = self.templocation
        out = repo.all()
        self.assertEqual(out, [])

    def test_If_no_provenance_known_for_file_byPath_raises_IndexError(self):
        from niprov.jsonfile import JsonFile
        serializer = Mock()
        serializer.deserializeList.return_value = []
        repo = JsonFile(json=serializer)
        repo.datafile = self.templocation
        with self.assertRaises(IndexError):
            repo.byPath('nothere')

    def test_Can_add_file_and_ask_whether_its_known(self):
        from niprov.jsonfile import JsonFile
        repo = JsonFile(factory=self.fileFactory)
        repo.datafile = self.templocation
        provenance = self.sampleProvenanceRecord()
        repo.add(provenance)
        repo2 = JsonFile(factory=self.fileFactory)
        repo2.datafile = self.templocation
        self.assertFalse(repo2.knowsByPath('nonexisting'))
        self.assertTrue(repo2.knowsByPath(provenance['path']))

    def test_Can_add_file_and_ask_whether_its_known(self):
        from niprov.jsonfile import JsonFile
        repo = JsonFile(factory=self.fileFactory)
        repo.datafile = self.templocation
        provenance = self.sampleProvenanceRecord()
        repo.add(provenance)
        repo2 = JsonFile(factory=self.fileFactory)
        repo2.datafile = self.templocation
        known = Mock()
        known.path = provenance['path']
        unknown = Mock()
        unknown.path = 'maohafnv'
        self.assertFalse(repo2.knows(unknown))
        self.assertTrue(repo2.knows(known))

    def test_Can_add_file_and_ask_whether_its_series_is_known(self):
        from niprov.jsonfile import JsonFile
        repo = JsonFile(factory=self.fileFactory)
        repo.datafile = self.templocation
        provenance = self.sampleProvenanceRecord()
        SUID = 'iamtheseries'
        provenance['seriesuid'] = SUID
        repo.add(provenance)
        repo2 = JsonFile(factory=self.fileFactory)
        repo2.datafile = self.templocation
        knownSeries = Mock()
        knownSeries.path = 'apath1'
        knownSeries.getSeriesId.return_value = SUID
        unknown = Mock()
        unknown.path = 'anotherpath'
        self.assertFalse(repo2.knows(knownSeries)) #file itself not know
        self.assertFalse(repo2.knowsSeries(unknown)) #other series not known
        self.assertTrue(repo2.knowsSeries(knownSeries)) #but this file's series known

    def test_Can_add_file_and_ask_whether_its_series_is_known(self):
        from niprov.jsonfile import JsonFile
        repo = JsonFile(factory=self.fileFactory)
        repo.datafile = self.templocation
        provenance = self.sampleProvenanceRecord()
        provenance['seriesuid'] = None
        repo.add(provenance)
        noneSeries = Mock()
        noneSeries.getSeriesId.return_value = None
        self.assertFalse(repo.knowsSeries(noneSeries))

    def test_Can_get_provenance_for_series_with_getSeries(self):
        from niprov.jsonfile import JsonFile
        repo = JsonFile(factory=self.fileFactory)
        repo.datafile = self.templocation
        prov1 = self.sampleProvenanceRecord()
        prov2 = self.sampleProvenanceRecord()
        prov2['seriesuid'] = 's8m3d0s2'
        repo.add(prov1)
        repo.add(prov2)
        img = Mock()
        img.getSeriesId.return_value = prov2['seriesuid']
        img2 = Mock()
        img2.getSeriesId.return_value = 'a9m2l4a8'
        out = repo.getSeries(img)
        self.fileFactory.fromProvenance.assert_called_with(prov2)
        self.assertEqual(out, self.fileFactory.fromProvenance())
        with self.assertRaises(IndexError):
            repo.getSeries(img2)

    def test_Update(self):
        from niprov.jsonfile import JsonFile
        repo = JsonFile(factory=self.fileFactory)
        repo.datafile = self.templocation
        provenance = self.sampleProvenanceRecord()
        repo.add(provenance)
        intermediate = copy.deepcopy(provenance)
        intermediate['newfield'] = 'newval'
        intermediate['subject'] = 'Jane Newman'
        repo3 = JsonFile(factory=self.fileFactory)
        repo3.datafile = self.templocation
        updatedImage = Mock()
        updatedImage.path = intermediate['path']
        updatedImage.provenance = intermediate
        repo3.update(updatedImage)
        repo4 = JsonFile(factory=self.fileFactory)
        repo4.datafile = self.templocation
        out = repo4.byPath(provenance['path'])
        self.fileFactory.fromProvenance.assert_called_with( intermediate)

    def test_ByPath_also_returns_series_if_filepath_among_it(self):
        from niprov.jsonfile import JsonFile
        repo = JsonFile(factory=self.fileFactory)
        repo.datafile = self.templocation
        provenance = self.sampleProvenanceRecord()
        provenance['filesInSeries'] = ['sfile1.f','sfile2.f']
        repo.add(provenance)
        repo2 = JsonFile(factory=self.fileFactory)
        repo2.datafile = self.templocation
        out = repo2.byPath('sfile1.f')
        self.fileFactory.fromProvenance.assert_called_with(provenance)
        with self.assertRaises(IndexError):
            repo2.byPath('sfile3.f')


    def sampleProvenanceRecord(self):
        record = {}
        record['path'] = str(random.randint(1000,9999))
        record['subject'] = 'John Doeish'
        record['protocol'] = 'T1 SENSE'
        record['acquired'] = datetime(2014, 8, 5, 12, 19, 14)
        return record



