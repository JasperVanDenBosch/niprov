#!/usr/bin/python
# -*- coding: UTF-8 -*-
import unittest
from mock import Mock
from datetime import datetime
import json


class SerializerTests(unittest.TestCase):

    def test_serialize_makes_acquired_field_a_string(self):
        from niprov.jsonserializing import JsonSerializer  
        serializer = JsonSerializer()
        record = {}
        record['acquired'] = datetime.now()
        out = serializer.serialize(record)
        self.assertEqual(json.loads(out)['acquired'], 
            record['acquired'].isoformat())

    def test_deserialize_makes_acquired_field_a_datetime_object(self):
        from niprov.jsonserializing import JsonSerializer  
        serializer = JsonSerializer()
        record = {}
        original = datetime.now()
        record['acquired'] = original.isoformat()      
        out = serializer.deserialize(json.dumps(record))
        self.assertEqual(out['acquired'], original)

    def test_serializeList_makes_acquired_field_a_string(self):
        from niprov.jsonserializing import JsonSerializer  
        serializer = JsonSerializer()
        record = {}
        record['acquired'] = datetime.now()
        out = serializer.serializeList([record])
        self.assertEqual(json.loads(out)[0]['acquired'], 
            record['acquired'].isoformat())


