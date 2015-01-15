#!/usr/bin/python
# -*- coding: UTF-8 -*-
import unittest
from mock import Mock
from datetime import datetime
import json
import random


class StorageTests(unittest.TestCase):

    def test_Can_add_file_and_retrieve_it(self):
        from niprov.jsonfile import JsonFile
        repo = JsonFile()
        provenance = self.sampleProvenanceRecord()
        repo.add(provenance)
        repo2 = JsonFile()
        out = repo2.byPath(provenance['path'])
        self.assertEqual(out, provenance)

    def test_If_file_doesnt_exist_all_returns_empty_list(self):
        from niprov.jsonfile import JsonFile
        filesys = Mock()
        filesys.read.side_effect = IOError(
            "[Errno 2] No such file or directory: 'provenance.json'")
        repo = JsonFile(filesys)
        out = repo.all()
        self.assertEqual(out, [])

    def test_If_no_provenance_known_for_file_byPath_raises_IndexError(self):
        from niprov.jsonfile import JsonFile
        serializer = Mock()
        serializer.deserializeList.return_value = []
        repo = JsonFile(json=serializer)
        with self.assertRaises(IndexError):
            repo.byPath('nothere')

    def sampleProvenanceRecord(self):
        record = {}
        record['path'] = str(random.randint(1000,9999))
        record['subject'] = 'John Doeish'
        record['protocol'] = 'T1 SENSE'
        record['acquired'] = datetime(2014, 8, 5, 12, 19, 14)
        return record



