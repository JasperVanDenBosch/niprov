#!/usr/bin/python
# -*- coding: UTF-8 -*-
import unittest
from mock import Mock
from datetime import datetime
import json
import random


class StorageTests(unittest.TestCase):

    def setUp(self):
        r = random.randint(1000,9999)
        self.templocation = '/var/tmp/provenance-{0}.json'.format(r)

    def test_Can_add_file_and_retrieve_it(self):
        from niprov.jsonfile import JsonFile
        repo = JsonFile()
        repo.datafile = self.templocation
        provenance = self.sampleProvenanceRecord()
        repo.add(provenance)
        repo2 = JsonFile()
        repo2.datafile = self.templocation
        out = repo2.byPath(provenance['path'])
        self.assertEqual(out, provenance)

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
        repo = JsonFile()
        repo.datafile = self.templocation
        provenance = self.sampleProvenanceRecord()
        repo.add(provenance)
        repo2 = JsonFile()
        repo2.datafile = self.templocation
        self.assertFalse(repo2.knowsByPath('nonexisting'))
        self.assertTrue(repo2.knowsByPath(provenance['path']))


    def sampleProvenanceRecord(self):
        record = {}
        record['path'] = str(random.randint(1000,9999))
        record['subject'] = 'John Doeish'
        record['protocol'] = 'T1 SENSE'
        record['acquired'] = datetime(2014, 8, 5, 12, 19, 14)
        return record



